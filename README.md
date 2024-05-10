# ReBeT: Architecture-based Self-adaptation of Robotic Systems through Behavior Trees
<!-- This repository is a companion page for the following publication:
> Author Names. Publication year. Thesis / Paper title. Publication venue / proceedings.

It contains all the material required for replicating the study, including: X, Y, and Z.

## How to cite us
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





### Re-doing the experiments
To be able to use this part of the replication package, you need to install docker: https://docs.docker.com/get-docker/ .
We provide a docker image (https://hub.docker.com/repository/docker/egalberts/rebetfrog/general) as an all-in-one solution for reproducing the evaluation of our work. We will now explain how it can be used:
1. Use the following command to create a container based on the image, which deletes itself upon stopping:   
   ```Bash
   docker run --rm  -it --shm-size=512m -p 6901:6901 -e VNC_PW=password egalberts/rebetfrog:acsos 
   ```
    note: depending on your OS and install, you may need to prepend the command with `sudo`.
2.Once it is running, using your web browser navigate to `localhost:6901`. You will be prompted for a username and password which are as follows:
 - **User** : `kasm_user`
 - **Password**: `password`

  note: The password is specified in the run command from step 1, and can be changed.

3. You should now find yourself looking at a desktop of virtual machine of Ubuntu 22. Within the virtual machine, use the file explorer to navigate to `/home/kasm-user/rebet_ws/`. Here you will find a build_all.sh scripts as well as a src folder and scripts folder. The former contains ReBeT's source code aligned with its repository (https://github.com/EGAlberts/ReBeT/tree/ACSOS), the latter contains scripts which run FROG alongside ReBeT as in the evaluation. Use the following command in a terminal inside this folder to build all of the ROS2 packages:
   ```Bash
   ./build_all.sh
   ```
   note: While there may be some warnins/error messages, unless the build explicitly fails and aborts itself, everything should be built correctly upon completion. This process should take around 3-5 minutes.
4. Now you are ready to reproduce the evaluation. Within the scripts folder we provide two scripts corresponding to the two subsections of our evaluation, namely `ACSOSEVAL1.sh` and `ACSOSEVAL2.sh`. You can simply use the following command in the same terminal you built in to get the ball rolling:
   ```Bash
   ./scripts/ACSOSEVAL1.sh
   ```
   This will open several terminals, including the gazebo simulator. Getting everything up and running can take roughly 1 minute. Then, without any user intervention FROG should begin its mission. If you would like to reproduce the entire evaluation, simply replace ACSOSEVAL1.sh with ACSOSEVAL2.sh in the above command. Please note, each run of this script takes at least 5 minutes, meaning running it to completion would take about 6 hours. Executing ACSOSEVAL1.sh is only one run, and takes about 5 minutes to complete. We recommend just running the above command if yuo would like to get an idea, and save the rest for anyone interested in extending our work.

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


