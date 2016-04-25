#!/bin/bash
echo $0 $1 $2

startDir=`pwd`
lockfile=${startDir}/op_tasks/SM_LOCK
rootDIR='/home/ubuntu'
venvPath=$rootDIR/sites/testing/venv
smPath=${rootDIR}/smbitBucket/SurveyMongo
scotchPath="${rootDIR}/SCOtCH"
matDIR="${rootDIR}/smbitBucket/SurveyMongo/reports"

source $venvPath/bin/activate

while [ -f $lockfile ]
do 
    # Run until lock file set by STOUT has cleared
    echo removing $lockfile
    rm $lockfile
    
    # Run SurveyMongo to update the Master Answer Table
    cd $smPath
    echo "spawning $smPath SurveyMongo db update ($1)"
    nice -n 10 python ./surveymongo_build_db.py --name $1
    echo "spawning $smPath SurveyMongo mat update ($1 $2)"
    nice -n 10 python ./surveymongo_build_mat.py --name $1 --exp $2
    
    echo "SCOtCH processing start!"


    # Process MAT With SCOtCH
    # copy the MAT data over to the scotch directory
    cp -f ${matDIR}/MOT_mat.csv ${scotchPath}

    # run scotch
    cd ${scotchPath}

    outputDate=$(date +%Y%m%d_%H%M%S)
    aggCheckFile="aggCheck_${outputDate}.csv"
    matFile="MasterAnswerTable_${outputDate}.csv"

    nice -n 10 Rscript --vanilla scotchArgs.R MOT_mat.csv codebook.scales.csv codebook.items.csv ${aggCheckFile} ${matFile}

    echo "SCOtCH processing complete!"
done

echo "SurveyMongo update complete!"
