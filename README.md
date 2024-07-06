# ReBeT: Architecture-based Self-adaptation of Robotic Systems through Behavior Trees
This repository is a companion page for the following publication:
> Elvin Alberts, Ilias Gerostathopoulos, Vincenzo Stoico, Patricia Lago. 2024. ReBeT: Architecture-based Self-adaptation of Robotic Systems through Behavior Trees. IEEE International Conference on Autonomic Computing and Self-Organizing Systems (ACSOS).

<!-- ## How to cite us
The scientific article describing design, execution, and main results of this study is available [here](https://www.google.com).<br> 
If this study is helping your research, consider to cite it is as follows, thanks!
```
@article{,
  title={},
  author={},
  journal={},
  volume={},
  pages={},
  year={},
  publisher={}
}
``` -->




## Getting started
To be able to use this replication package, you need to install docker: https://docs.docker.com/get-docker/. We provide it as a docker image due to ROS2 requiring Ubuntu, followed by many installations. 

If for whatever reason you do not or cannot use docker, but do have access to Ubuntu 22, to install from source execute the install_rebet.sh script found inside docker/installation_scripts/. Please note it does assume you have installed ROS2 Humble yourself first.

To create a docker container based on the docker image containing the artifact, please use the following command:

   ```Bash
   docker run --rm  -p 6080:80 --privileged --name acsos_artifact egalberts/rebet:acsos 
   ```
The --rm option here indicates the upon closing the container it will delete itself to conserve space. After executing the command it will begin downloading the image. Note: this may take a while. When the download is complete it will create and run the container, the terminal should eventually output something like: "vnc entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)". This indicates the container is ready to be used.

## Execution
While the container is running, you can open a GUI to it through your web browser. Use your preferred web browser to navigate to `http://localhost:6080` . Note, if for whatever reason port `6080` is in use on your machine, you can change it in the docker run command above to whatever you like, and make sure to reflect that change in the URL used in your web browser. 

### Reproducing the Evaluation

Within the web-based GUI, navigate to the Home folder (shortcut on the desktop), there you should find a folder named `rebet_ws`. Within this folder you will find the source code, and built packages, of a variety of open source packages including that of our own work ReBeT. You can find the version used for the artifact here: https://github.com/EGAlberts/ReBeT/tree/ACSOS.

Within the scripts folder, there are two main shell scripts corresponding to the two evaluations in the paper namely `ACSOSEVAL1.sh` and `ACSOSEVAL2.sh`. We provide two versions of these, with gui and without gui. This pertains to the Gazebo simulation visually simulating the robot or not.For weaker machines, especially considering the usage of docker we recommend first testing it out with no gui. You can simply use the following command in the same terminal you built in to get the ball rolling:
   ```Bash
   ./scripts/ACSOSEVAL1_nogui.sh
   ```


Note: Do not use Terminator for runnning the above, but the MATE Terminal (Click on Menu on the top left, then System Tools to find the MATE Terminal) as terminator conflicts with opening multiple terminals.


   This will open several terminals, including the gazebo simulator. Getting everything up and running can take roughly 1 minute. Then, without any user intervention FROG should begin its mission. If you would like to reproduce the entire evaluation, simply replace ACSOSEVAL1.sh with ACSOSEVAL2.sh in the above command. Please note, each run of this script takes at least 5 minutes, meaning running it to completion would take about 6 hours. Executing ACSOSEVAL1.sh is only one run, and takes about 5 minutes to complete.

Each time a run completes, it produces a timestamped CSV file in the scripts folder with the results of that run. This details things such as the satisfaction of various quality requirements in effect, and the adaptations in effect, on a second-by-second basis.  

For doing a run with the gui, simply replace nogui with gui in the command above.
Please note that the csv produced is the same for both evaluations, meaning depending on which one was run the csv contains filler data. For EVAL1, you can confirm a successful run by looking at the 'current_task' column, which alternates between charging and visitingFrontier, depending on the value of the column power_status. For EVAL2, the inverse should be considered, and it is a lot clearer. When in doubt, please take a look at the data used for the Analysis section below.

### Extensions

It is easy to modify and extend ReBeT. The first place to look to get an understanding is the specification of the behavior trees, in the folder src/rebet/rebet/trees/. All the trees starting with 'frog_' are used in the different parts of the evaluations. In these xml files one can modify minor things with only a simple rebuild necessary, such as the adaptation period used for changing the maximum speed. Within the source code, existing QRDecorators can be modified to experiment with different constraints, or new ones can be introduced. For truly extending ReBeT, we recommend using the main branch of ReBeT https://github.com/EGAlberts/ReBeT/ which we are actively developing, and has been refined thoroughly since the submission to ACSOS.

To help explain, we provide a short example of making a change:

The change we will make involves the battery percentage maintained by the QR in EVAL1.
If you navigate to `/home/ubuntu/rebet_ws/src/rebet/include/rebet_frog`, you will find a file called `frog_qrs.h`. You can open this using the pre-installed VSCodium IDE. On line 520 we begin defining the SystemPowerQR, which is remapped to KeepBatteryMin in the BT used in EVAL1. Here, on line 655 the threshold for charging is defined. Once more than 40W have been consumed, the battery is considered too empty as it is currently defined. You can change the constant to 80, leading to twice as much exploration before charging occurs. 

Once you have made a change, navigate back to `/home/ubuntu/rebet_ws/`, and run the following command to compile your changes.

```Bash
colcon build --packages-select rebet
```
You may see some warnings, but unless the build explictly fails, your changes should now be applied. The above command can be used to apply changes made anywhere within the rebet package. You can simply use the same commands explain earlier to reproduce the evaluation with your chosen changes and to see their effect. With our example, the effect should be that charging happens more less often.

Please note: We strove to introduce as few changes as possible to the code provided in the artifact, to provide an identical setup to what was used to produce the results presented in the paper. This means that some parts of the source code are not very refined.

### Analysis of the results
Here we cover reproducing the plots and parsing of data for the evaluations. You need to have Python 3 installed. We provide all the data we used, so it is not necessary to do any of the experiments yourself to look at the source of our results.

0. Clone this repository, and use the following command in a terminal in the cloned folder to install the dependencies for the analysis scripts.
    ```Bash
   pip install -r src/requirements.txt
   ```
   
1. You can use the following command to produce the plot of the first evaluation:
      ```Bash
   python src/evaluationA.py
   ```
   note: On your system python 3 may use the command `python3` rather than `python`, if so please replace `python` with `python3` in the above command.

2. To reproduce the tables and analyses done for the results of the second evaluation, please use the following command within the cloned repository folder:
   ```Bash
   python src/evaluationB.py
   ```
These python scripts parse the csv files found under the subfolders of the data folder, which you can also view directly. Each csv represents a singular execution of the mission.


