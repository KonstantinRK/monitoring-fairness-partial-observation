#!/bin/bash
#
#----------------------------------------------------------------
# running a multiple independent jobs
#----------------------------------------------------------------
#


#  Defining options for slurm how to run
#----------------------------------------------------------------
#
#SBATCH --job-name=RV23
#SBATCH --output=RV23_%A-%a.log
#        %A and %a are placeholders for the jobid and taskid, resp.
#
#Number of CPU cores to use within one node
#SBATCH -c 1
#
#Define the number of hours the job should run.
#Maximum runtime is limited to 10 days, ie. 240 hours
#SBATCH --time=48:00:00
#
#Define the amount of RAM used by your job in GigaBytes
#In shared memory applications this is shared among multiple CPUs
#SBATCH --mem=600G
#
#Send emails when a job starts, it is finished or it exits
#SBATCH --mail-user=konstantin.kueffner@ista.ac.at
#SBATCH --mail-type=ALL
#
#Do not requeue the job in the case it fails.
#SBATCH --no-requeue
#
#Do not export the local environment to the compute nodes
#SBATCH --export=NONE
unset SLURM_EXPORT_ENV

# load the respective software module(s) you intend to use
#----------------------------------------------------------------
module load python/3.10

# define sequence of jobs to run as you would do in a BASH script
# use variable $SLURM_ARRAY_TASK_ID to address individual behaviour
# in different iteration of the script execution
#----------------------------------------------------------------

srun python /nfs/scistore16/tomgrp/kkueffne/RV_23_cluster_upload/run_experiments.py ${SLURM_ARRAY_TASK_ID}

