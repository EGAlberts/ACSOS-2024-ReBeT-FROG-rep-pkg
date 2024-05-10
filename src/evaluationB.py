import pandas as pd
import glob
from scipy.stats import mannwhitneyu

SAFETY_QR = "safety_metric"
MOVEFF_QR = "movement_efficiency"
MOVPOW_QR = "move_pow_metric"
PIC_TAKEN = "pics_taken" 
CAM_TOP = "curr_cam_topic"
DET_EFF = "obj_det_eff"
OBJ_POW = "obj_power"

WAFFLE_MAX_LIN_VEL = 0.26
SAFETY_SPEED_REQ = 0.18
PROXIMITY_SAFETY_THRESHOLD = 0.10
LOW_SPEED_SAFETY_THRESHOLD = SAFETY_SPEED_REQ/WAFFLE_MAX_LIN_VEL

DUMMY_VALUE = -10
DUMMY_VALUE_STR = "-10.0"
ALT_CAM_VALUE = "/corner_camera/image_raw"
SIGNIFIGANCE = 0.05


def statistical_test(x,y):
    _, p_det = mannwhitneyu(x["U_det"],y["U_det"],alternative="greater")
    _, p_vis = mannwhitneyu(x["U_vis"],y["U_vis"],alternative="greater")

    print('p_det={:.20f} , p_vis={:.20f}'.format(p_det,p_vis))
    print((p_det,p_vis))

    print("p_det significant?" + str(p_det < SIGNIFIGANCE))
    print("p_vis significant?" + str(p_vis < SIGNIFIGANCE))





def analyze_results(folder_path):
    csv_files =  glob.glob(folder_path + '/*.csv')

    res_df_dic = {}

    for res_csv in csv_files:
        res_df_dic[res_csv.split("/")[-1]] = pd.read_csv(res_csv)
    df = pd.DataFrame(index=res_df_dic.keys())


    for curr_key in res_df_dic.keys():

        res_df = res_df_dic[curr_key]


        is_safety_qr_satisfied = (res_df[res_df[SAFETY_QR] != DUMMY_VALUE][SAFETY_QR] > PROXIMITY_SAFETY_THRESHOLD) & (res_df[res_df[MOVEFF_QR] != DUMMY_VALUE][MOVEFF_QR] < LOW_SPEED_SAFETY_THRESHOLD)

        is_deteff_qr_satisfied = res_df[res_df[DET_EFF] != DUMMY_VALUE_STR][DET_EFF].str.split(',', n=1, expand=True)

        velocity_ratio = res_df[res_df[MOVEFF_QR] != DUMMY_VALUE][MOVEFF_QR] 
        inverted_power = (1/res_df[(res_df[MOVPOW_QR] != DUMMY_VALUE)][MOVPOW_QR])

        df.loc[curr_key, 'U_vis'] = (is_safety_qr_satisfied.astype(int) * velocity_ratio * inverted_power).mean()

        is_power_budget_satisfied = res_df[(res_df[OBJ_POW] != DUMMY_VALUE) & (res_df[CAM_TOP] != ALT_CAM_VALUE)][OBJ_POW] > 0


        pictures_taken = pd.to_numeric(is_deteff_qr_satisfied[1]).max()
        target_detected = pd.to_numeric(is_deteff_qr_satisfied[0]).max()

        df.loc[curr_key, 'inv_pow'] = velocity_ratio.mean()
        df.loc[curr_key, 'vel_rat'] = inverted_power.mean()
        df.loc[curr_key, 'p_rat'] = (target_detected /  pictures_taken)
        df.loc[curr_key, 'U_det'] = (is_power_budget_satisfied.astype(int) * (target_detected /  pictures_taken)).mean()

    df_mean = df.mean()
    df_std = df.std()

    report_def = pd.concat([df_mean, df_std], axis=1)
    report_def.columns = ['Mean', 'Std Dev.']

    return df, report_def

# Example usage:
internal_path = 'data/EvaluationB/internal'
baseline_path = 'data/EvaluationB/baseline'
external_path = 'data/EvaluationB/external'



df_internal, df_internal_rep = analyze_results(internal_path)
df_baseline, df_baseline_rep = analyze_results(baseline_path)
df_external, df_external_rep = analyze_results(external_path)



print("BASELINE:")
print(df_baseline)
print("--" * 20)
print("INTERNAL:")
print(df_internal)
print("--" * 20)
print("EXTERNAL:")
print(df_external)
print("--" * 20)

print(" " * 20)
print(" " * 20)

print("BASELINE:")
print(df_baseline_rep)
print("--" * 20)
print("INTERNAL:")
print(df_internal_rep)
print("--" * 20)
print("EXTERNAL:")
print(df_external_rep)
print("--" * 20)

print(" " * 20)
print(" " * 20)


print("Internal Statistical Test:")
statistical_test(df_internal,df_baseline)
print(" " * 20)
print(" " * 20)
print("External Statistical Test:")
statistical_test(df_external,df_baseline)

exit(0)