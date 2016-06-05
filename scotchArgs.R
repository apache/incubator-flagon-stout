#!/usr/bin/env Rscript

# Usage: This script uses reads in static files produced by STOUT that include form data from other services (e.g., SurveyMonkey)
#and experiment data from STOUT, and timing data collected through a STOUT User ALE instance. 
##It runs:
###basic "truthing" (is form entry right or wrong), 
###"timing corrections" (client (STOUT time) vs. 3rd party timing), and
###post-processing operations (scale mean calculation, basic statistics)
###prints new version of STOUT data with appendended fields (variables), and values.

#--------------------------------------------------------------------------------------------------------------
# Data Ingest 
##Read in static files from STOUT

# Rscript --vanilla scotchArgs.R working.merge.csv xdata.codebook.yr3.v2.scales.csv xdata.codebook.yr3.v2.items.csv aggCheck.csv MasterAnswerTable.csv
args = commandArgs(trailingOnly=TRUE)

# input files:
matDataFile = "working.merge.csv"
codeBookScalesFile = "xdata.codebook.MOTv4.scales.csv"
codeBookItemsFile = "xdata.codebook.MOTv4.items.csv"
# output files:
aggCheckFile = "aggCheck.csv"
matFile = "MasterAnswerTable.csv"

if (length(args)>=1) {
  matDataFile = args[1]
  if (length(args)>=2) {
    codeBookScalesFile = args[2]
    if (length(args)>=3) {
      codeBookItemsFile = args[3]
      if (length(args)>=4) {
        aggCheckFile = args[4]
        if (length(args)>=5) {
          matFile = args[5]
        }
      }
    }
  }
} 



# raw data file as .csv into Data Frames
raw.data <- read.csv(matDataFile, header=TRUE, stringsAsFactors=FALSE)
colnames(raw.data)[colnames(raw.data)=="user_hash"] <- "SYS.IND.SESS."

codebook.scales <- read.csv(codeBookScalesFile, header=TRUE, stringsAsFactors=FALSE)      # create dataframe to hold codebook subscale metadata
row.names(codebook.scales) <- make.names(codebook.scales[,"varnames"], unique=TRUE)
codebook.items <- read.csv(codeBookItemsFile, header=TRUE, stringsAsFactors=FALSE)           # create dataframe to hold codebook items metadata
row.names(codebook.items) <- make.names(codebook.items[,"varnames"], unique=TRUE)


#--------------------------------------------------------------------------------------------------------------
#Truthing Script
##This script compares correct answers from Codebook to responses collected through form data

OTdataRaw.CP1 <- cbind(raw.data[,"SYS.IND.SESS."], subset(raw.data, select = (grepl("TSK.PRB.CP1.",names(raw.data))==TRUE))) # create working dataset from raw
names(OTdataRaw.CP1)[1] <- "SYS.IND.SESS."
OTdataRaw.CP2 <- cbind(raw.data[,"SYS.IND.SESS."], subset(raw.data, select = (grepl("TSK.PRB.CP2.",names(raw.data))==TRUE))) # create working dataset from raw
names(OTdataRaw.CP2)[1] <- "SYS.IND.SESS."
OTdataRaw.CP3 <- cbind(raw.data[,"SYS.IND.SESS."], subset(raw.data, select = (grepl("TSK.PRB.CP3.",names(raw.data))==TRUE))) # create working dataset from raw
names(OTdataRaw.CP3)[1] <- "SYS.IND.SESS."
OTdataRaw.CP4 <- cbind(raw.data[,"SYS.IND.SESS."], subset(raw.data, select = (grepl("TSK.PRB.CP4.",names(raw.data))==TRUE))) # create working dataset from raw
names(OTdataRaw.CP4)[1] <- "SYS.IND.SESS."
OTdataRaw.CP5 <- cbind(raw.data[,"SYS.IND.SESS."], subset(raw.data, select = (grepl("TSK.PRB.CP5.",names(raw.data))==TRUE))) # create working dataset from raw
names(OTdataRaw.CP5)[1] <- "SYS.IND.SESS."

# write truthing dataframe for each challenge problem, with common case index with working dataset, and name index column.
truth.cp1.data <- as.data.frame(cbind.data.frame(OTdataRaw.CP1[,"SYS.IND.SESS."], "TSK.PRB.ANS.CP1.OT1.001." = 0,"TSK.PRB.ANS.CP1.OT1.002." = 0,"TSK.PRB.ANS.CP1.OT1.003." = 0,"TSK.PRB.ANS.CP1.OT1.004." =0, "TSK.PRB.ANS.CP1.OT1.005." =0,"TSK.PRB.ANS.CP1.OT2.001." = 0,"TSK.PRB.ANS.CP1.OT2.003." = 0,"TSK.PRB.ANS.CP1.OT2.004." = 0,"TSK.PRB.ANS.CP1.OT2.005." = 0), stringsAsFactors=FALSE)
truth.cp2.data <- as.data.frame(cbind.data.frame(OTdataRaw.CP2[,"SYS.IND.SESS."], "TSK.PRB.ANS.CP2.OT1.001." = 0,"TSK.PRB.ANS.CP2.OT1.002." = 0,"TSK.PRB.ANS.CP2.OT1.003." = 0,"TSK.PRB.ANS.CP2.OT1.004." =0, "TSK.PRB.ANS.CP2.OT1.005." =0,"TSK.PRB.ANS.CP2.OT2.001." = 0,"TSK.PRB.ANS.CP2.OT2.002." = 0,"TSK.PRB.ANS.CP2.OT2.003." = 0,"TSK.PRB.ANS.CP2.OT2.004." = 0,"TSK.PRB.ANS.CP2.OT2.005." = 0), stringsAsFactors=FALSE)
truth.cp3.data <- as.data.frame(cbind.data.frame(OTdataRaw.CP3[,"SYS.IND.SESS."], "TSK.PRB.ANS.CP3.OT1.005.CGBI." = 0, "TSK.PRB.ANS.CP3.OT1.005.AERG." = 0, "TSK.PRB.ANS.CP3.OT1.005.MMTRS." = 0, "TSK.PRB.ANS.CP3.OT1.005.PGFY." = 0, "TSK.PRB.ANS.CP3.OT1.001." = 0, "TSK.PRB.ANS.CP3.OT1.004." = 0, "TSK.PRB.ANS.CP3.OT1.002." = 0, "TSK.PRB.ANS.CP3.OT1.003." = 0, "TSK.PRB.ANS.CP3.OT2.001.1ST." = 0, "TSK.PRB.ANS.CP3.OT2.001.2ND." = 0, "TSK.PRB.ANS.CP3.OT2.002.PZOO." = 0, "TSK.PRB.ANS.CP3.OT2.002.QMCI." = 0, "TSK.PRB.ANS.CP3.OT2.002.IMLE." = 0, "TSK.PRB.ANS.CP3.OT2.002.IMMB." = 0, "TSK.PRB.ANS.CP3.OT2.002.AHII." = 0, "TSK.PRB.ANS.CP3.OT2.002.GOOO." = 0, "TSK.PRB.ANS.CP3.OT2.002.FNRG." = 0, "TSK.PRB.ANS.CP3.OT2.003." = 0, "TSK.PRB.ANS.CP3.OT2.004.JAN." = 0, "TSK.PRB.ANS.CP3.OT2.004.FEB." = 0, "TSK.PRB.ANS.CP3.OT2.004.MAR." = 0, "TSK.PRB.ANS.CP3.OT2.004.APR." = 0, "TSK.PRB.ANS.CP3.OT2.004.MAY." = 0, "TSK.PRB.ANS.CP3.OT2.004.JUN." = 0, "TSK.PRB.ANS.CP3.OT2.004.JUL." = 0, "TSK.PRB.ANS.CP3.OT2.004.AUG." = 0, "TSK.PRB.ANS.CP3.OT2.004.SEP." = 0, "TSK.PRB.ANS.CP3.OT2.004.OCT." = 0, "TSK.PRB.ANS.CP3.OT2.004.NOV." = 0, "TSK.PRB.ANS.CP3.OT2.004.DEC." = 0, "TSK.PRB.ANS.CP3.OT2.005.GHIL." = 0, "TSK.PRB.ANS.CP3.OT2.005.IFLM." = 0, "TSK.PRB.ANS.CP3.OT2.005.FNRG." = 0, "TSK.PRB.ANS.CP3.OT2.005.CTOT." = 0, "TSK.PRB.ANS.CP3.OT2.005.CMGO." = 0, "TSK.PRB.ANS.CP3.OT2.005.MYRY." = 0), stringsAsFactors=FALSE)
truth.cp4.data <- as.data.frame(cbind.data.frame(OTdataRaw.CP4[,"SYS.IND.SESS."], "TSK.PRB.ANS.CP4.OT1.001." = 0,"TSK.PRB.ANS.CP4.OT1.002." = 0,"TSK.PRB.ANS.CP4.OT1.003." = 0,"TSK.PRB.ANS.CP4.OT2.001." = 0,"TSK.PRB.ANS.CP4.OT2.002." = 0,"TSK.PRB.ANS.CP4.OT2.003." = 0), stringsAsFactors=FALSE)
truth.cp5.data <- as.data.frame(cbind.data.frame(OTdataRaw.CP5[,"SYS.IND.SESS."], "TSK.PRB.ANS.CP5.OT1.001." = 0,"TSK.PRB.ANS.CP5.OT1.002." = 0,"TSK.PRB.ANS.CP5.OT1.003." = 0,"TSK.PRB.ANS.CP5.OT1.004." =0, "TSK.PRB.ANS.CP5.OT2.001." = 0,"TSK.PRB.ANS.CP5.OT2.002." = 0,"TSK.PRB.ANS.CP5.OT2.003." = 0,"TSK.PRB.ANS.CP5.OT2.004." = 0,"TSK.PRB.ANS.CP5.OT2.005." = 0), stringsAsFactors=FALSE)

names(truth.cp1.data)[1] <- "SYS.IND.SESS."
names(truth.cp2.data)[1] <- "SYS.IND.SESS."
names(truth.cp3.data)[1] <- "SYS.IND.SESS."
names(truth.cp4.data)[1] <- "SYS.IND.SESS."
names(truth.cp5.data)[1] <- "SYS.IND.SESS."

truthCalc = function(ind, ans, rawData, codebook, truthData){
  # arguments:
  #   ind = the variable being checked
  #   ans = the variable name containing the truth
  #   rawData = dataframe holding participant data being checked
  #   codebook = dataframe containing correct answers and the weights for each
  #   truthData = dataframe holding the truthed data
  
  truths = strsplit(codebook[ind,"truth"],split=",")  # each "truth" cell in the codebook contains all the strings such that if any are in the answer, it is correct; this command splits the contents of the truth cell into those strings
  for(i in 1:nrow(rawData)){ # for each case in the raw data
    flagCorrect = FALSE   # the answer is wrong until a match is found
    if(length(truths[[1]])>0) {
      for(n in 1:length(truths[[1]])){  # for all the strings that need to be checked (if no commas, length equals 1, containing the contents that are in the truth cell)          
        if(!is.na(rawData[i,ind])){     #if cell is not empty        
          if(grepl(paste("\\<" ,truths[[1]][[n]],"\\>",sep=""), rawData[i,ind], ignore.case=TRUE)==TRUE){  # paste truth from codebook, then \\<word\\> match on complete string sequence against cell content
            flagCorrect = TRUE          # if a match is found, then mark the answer as correct
          }
        }
      }
    }
    if(flagCorrect == TRUE){ truthData[i, ans] = 1 } # if the answer was flagged correct
  } 
  truthCalc = truthData   # return the truth data
}

truthCalcExactMatch = function(ind, ans, rawData, codebook, truthData){
  # arguments:
  #   ind = the variable being checked
  #   ans = the variable name containing the truth
  #   rawData = dataframe holding participant data being checked
  #   codebook = dataframe containing correct answers and the weights for each
  #   truthData = dataframe holding the truthed data
  
  truths = strsplit(codebook[ind,"truth"],split=",")  # each "truth" cell in the codebook contains all the strings such that if any are in the answer, it is correct; this command splits the contents of the truth cell into those strings
  for(i in 1:nrow(rawData)){ # for each case in the raw data
    flagCorrect = FALSE   # the answer is wrong until a match is found
    for(n in 1:length(truths[[1]])){  # for all the strings that need to be checked (if no commas, length equals 1, containing the contents that are in the truth cell)   
      if(!is.na(rawData[i,ind])){     #if cell is not empty
        if(grepl(paste("^" ,truths[[1]][[n]],"$",sep=""), rawData[i,ind], ignore.case=TRUE)==TRUE){  # paste truth from codebook, then \\<word\\> match on complete string sequence against cell content
          flagCorrect = TRUE          # if a match is found, then mark the answer as correct
        }
      }
    }
    if(flagCorrect == TRUE){ truthData[i, ans] = 1 } # if the answer was flagged correct
  } 
  truthCalcExactMatch = truthData   # return the truth data
}


#------------------------------------------------------------------------------
# CP1. Population Movements
#------------------------------------------------------------------------------

truth.cp1.data = truthCalc("TSK.PRB.CP1.OT1.001.", "TSK.PRB.ANS.CP1.OT1.001.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT1.002.", "TSK.PRB.ANS.CP1.OT1.002.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT1.003.", "TSK.PRB.ANS.CP1.OT1.003.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT1.004.", "TSK.PRB.ANS.CP1.OT1.004.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT1.005.", "TSK.PRB.ANS.CP1.OT1.005.", OTdataRaw.CP1, codebook.items, truth.cp1.data)

truth.cp1.data = truthCalc("TSK.PRB.CP1.OT2.001.", "TSK.PRB.ANS.CP1.OT2.001.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
#truth.cp1.data = truthCalc("TSK.PRB.CP1.OT2.002.", "TSK.PRB.ANS.CP1.OT2.002.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT2.003.", "TSK.PRB.ANS.CP1.OT2.003.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT2.004.", "TSK.PRB.ANS.CP1.OT2.004.", OTdataRaw.CP1, codebook.items, truth.cp1.data)
truth.cp1.data = truthCalc("TSK.PRB.CP1.OT2.005.", "TSK.PRB.ANS.CP1.OT2.005.", OTdataRaw.CP1, codebook.items, truth.cp1.data)

#write.csv(truth.cp1.data, file = "CP1_Truthv3_Check.csv", row.names=FALSE) # write out the data


#------------------------------------------------------------------------------
# CP2. Dealiasing
#------------------------------------------------------------------------------

truth.cp2.data = truthCalc("TSK.PRB.CP2.OT1.001.", "TSK.PRB.ANS.CP2.OT1.001.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT1.002.", "TSK.PRB.ANS.CP2.OT1.002.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT1.003.", "TSK.PRB.ANS.CP2.OT1.003.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT1.004.", "TSK.PRB.ANS.CP2.OT1.004.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT1.005.", "TSK.PRB.ANS.CP2.OT1.005.", OTdataRaw.CP2, codebook.items, truth.cp2.data)

truth.cp2.data = truthCalc("TSK.PRB.CP2.OT2.001.", "TSK.PRB.ANS.CP2.OT2.001.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT2.002.", "TSK.PRB.ANS.CP2.OT2.002.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT2.003.", "TSK.PRB.ANS.CP2.OT2.003.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT2.004.", "TSK.PRB.ANS.CP2.OT2.004.", OTdataRaw.CP2, codebook.items, truth.cp2.data)
truth.cp2.data = truthCalc("TSK.PRB.CP2.OT2.005.", "TSK.PRB.ANS.CP2.OT2.005.", OTdataRaw.CP2, codebook.items, truth.cp2.data)

#write.csv(truth.cp2.data, file = "CP2_Truthv3_Check.csv", row.names=FALSE)

#------------------------------------------------------------------------------
# CP3. Financial
#------------------------------------------------------------------------------

truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.005.CGBI.", "TSK.PRB.ANS.CP3.OT1.005.CGBI.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.005.AERG.", "TSK.PRB.ANS.CP3.OT1.005.AERG.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.005.MMTRS.", "TSK.PRB.ANS.CP3.OT1.005.MMTRS.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.005.PGFY.", "TSK.PRB.ANS.CP3.OT1.005.PGFY.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.001.", "TSK.PRB.ANS.CP3.OT1.001.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.004.", "TSK.PRB.ANS.CP3.OT1.004.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.002.", "TSK.PRB.ANS.CP3.OT1.002.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT1.003.", "TSK.PRB.ANS.CP3.OT1.003.", OTdataRaw.CP3, codebook.items, truth.cp3.data)

# truthing for TSK.PRB.CP3.OT2.001.1ST.
for(i in 1:nrow(OTdataRaw.CP3)){
  if(is.null(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."])==FALSE){
    
    dateTemp1 = as.Date("2000-01-01")
    
    if(nchar(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."])<8){ OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."] = paste("0", OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."], sep = "")}
    
    if(!is.na(as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."], "%m%d%Y"))){
      dateTemp1 = as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."], "%m%d%Y")
    } else if(!is.na(as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."], "%m/%d/%Y"))){ 
      dateTemp1 = as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.1ST."], "%m/%d/%Y")
    }
    
    if((dateTemp1 >= as.Date("2014-01-01")) && (dateTemp1 <= as.Date("2014-05-31"))){
      truth.cp3.data[i, "TSK.PRB.ANS.CP3.OT2.001.1ST."] = 1
    }
    
  }
}

# truthing for TSK.PRB.CP3.OT2.001.2ND.
for(i in 1:nrow(OTdataRaw.CP3)){
  if(is.null(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."])==FALSE){
    
    dateTemp1 = as.Date("2000-01-01")
    
    if(nchar(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."])<8){ OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."] = paste("0", OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."], sep = "")}
    
    if(!is.na(as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."], "%m%d%Y"))){
      dateTemp1 = as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."], "%m%d%Y")
    } else if(!is.na(as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."], "%m/%d/%Y"))){ 
      dateTemp1 = as.Date(OTdataRaw.CP3[i,"TSK.PRB.CP3.OT2.001.2ND."], "%m/%d/%Y")
    }
    
    if((dateTemp1 >= as.Date("2015-01-01")) && (dateTemp1 <= as.Date("2015-03-31"))){
      truthData[i, "TSK.PRB.ANS.CP3.OT2.001.2ND."] = 1
    }
    
  }
}

truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.PZOO.", "TSK.PRB.ANS.CP3.OT2.002.PZOO.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.QMCI.", "TSK.PRB.ANS.CP3.OT2.002.QMCI.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.IMLE.", "TSK.PRB.ANS.CP3.OT2.002.IMLE.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.IMMB.", "TSK.PRB.ANS.CP3.OT2.002.IMMB.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.AHII.", "TSK.PRB.ANS.CP3.OT2.002.AHII.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.GOOO.", "TSK.PRB.ANS.CP3.OT2.002.GOOO.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalcExactMatch("TSK.PRB.CP3.OT2.002.FNRG.", "TSK.PRB.ANS.CP3.OT2.002.FNRG.", OTdataRaw.CP3, codebook.items, truth.cp3.data)

truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.003.", "TSK.PRB.ANS.CP3.OT2.003.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.JAN.", "TSK.PRB.ANS.CP3.OT2.004.JAN.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.FEB.", "TSK.PRB.ANS.CP3.OT2.004.FEB.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.MAR.", "TSK.PRB.ANS.CP3.OT2.004.MAR.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.APR.", "TSK.PRB.ANS.CP3.OT2.004.APR.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.MAY.", "TSK.PRB.ANS.CP3.OT2.004.MAY.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.JUN.", "TSK.PRB.ANS.CP3.OT2.004.JUN.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.JUL.", "TSK.PRB.ANS.CP3.OT2.004.JUL.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.AUG.", "TSK.PRB.ANS.CP3.OT2.004.AUG.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.SEP.", "TSK.PRB.ANS.CP3.OT2.004.SEP.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.OCT.", "TSK.PRB.ANS.CP3.OT2.004.OCT.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.NOV.", "TSK.PRB.ANS.CP3.OT2.004.NOV.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.004.DEC.", "TSK.PRB.ANS.CP3.OT2.004.DEC.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.005.GHIL.", "TSK.PRB.ANS.CP3.OT2.005.GHIL.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.005.IFLM.", "TSK.PRB.ANS.CP3.OT2.005.IFLM.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.005.FNRG.", "TSK.PRB.ANS.CP3.OT2.005.FNRG.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.005.CTOT.", "TSK.PRB.ANS.CP3.OT2.005.CTOT.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.005.CMGO.", "TSK.PRB.ANS.CP3.OT2.005.CMGO.", OTdataRaw.CP3, codebook.items, truth.cp3.data)
truth.cp3.data = truthCalc("TSK.PRB.CP3.OT2.005.MYRY.", "TSK.PRB.ANS.CP3.OT2.005.MYRY.", OTdataRaw.CP3, codebook.items, truth.cp3.data)

truth.cp3.data = cbind(truth.cp3.data,rowSums(subset(truth.cp3.data, select = c(TSK.PRB.ANS.CP3.OT1.005.CGBI.,TSK.PRB.ANS.CP3.OT1.005.PGFY.), na.rm = TRUE)))
names(truth.cp3.data)[ncol(truth.cp3.data)] <- "TSK.PRB.ANS.CP3.OT1.005."
truth.cp3.data = cbind(truth.cp3.data,rowSums(subset(truth.cp3.data, select = (grepl("TSK.PRB.ANS.CP3.OT2.001.", names(truth.cp3.data))==TRUE)), na.rm = TRUE))
names(truth.cp3.data)[ncol(truth.cp3.data)] <- "TSK.PRB.ANS.CP3.OT2.001."
truth.cp3.data = cbind(truth.cp3.data,rowSums(subset(truth.cp3.data, select = (grepl("TSK.PRB.ANS.CP3.OT2.002.", names(truth.cp3.data))==TRUE)), na.rm = TRUE))
names(truth.cp3.data)[ncol(truth.cp3.data)] <- "TSK.PRB.ANS.CP3.OT2.002."
truth.cp3.data = cbind(truth.cp3.data,rowSums(subset(truth.cp3.data, select = c(TSK.PRB.ANS.CP3.OT2.004.OCT.,TSK.PRB.ANS.CP3.OT2.004.NOV.), na.rm = TRUE)))
names(truth.cp3.data)[ncol(truth.cp3.data)] <- "TSK.PRB.ANS.CP3.OT2.004."
truth.cp3.data = cbind(truth.cp3.data,rowSums(subset(truth.cp3.data, select = (grepl("TSK.PRB.ANS.CP3.OT2.005.", names(truth.cp3.data))==TRUE)), na.rm = TRUE))
names(truth.cp3.data)[ncol(truth.cp3.data)] <- "TSK.PRB.ANS.CP3.OT2.005."

truth.cp3.data.agg <- subset(truth.cp3.data, select= unlist(lapply(gregexpr("\\.",names(truth.cp3.data)),length)) < 7)
                      
#write.csv(truth.cp3.data, file = "CP3_Truthv3_Check.csv", row.names=FALSE)

#------------------------------------------------------------------------------
# CP4. Population Movements for GEQE
#------------------------------------------------------------------------------

truth.cp4.data = truthCalc("TSK.PRB.CP4.OT1.001.1ST.", "TSK.PRB.ANS.CP4.OT1.001.1ST.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
truth.cp4.data = truthCalc("TSK.PRB.CP4.OT1.001.2ND.", "TSK.PRB.ANS.CP4.OT1.001.2ND.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
truth.cp4.data = truthCalc("TSK.PRB.CP4.OT1.002.", "TSK.PRB.ANS.CP4.OT1.002.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
truth.cp4.data = truthCalc("TSK.PRB.CP4.OT1.003.", "TSK.PRB.ANS.CP4.OT1.003.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
#truth.cp4.data = truthCalc("TSK.PRB.CP4.OT1.004.", "TSK.PRB.ANS.CP4.OT1.004.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
#truth.cp4.data = truthCalc("TSK.PRB.CP4.OT1.005.", "TSK.PRB.ANS.CP4.OT1.005.", OTdataRaw.CP4, codebook.items, truth.cp4.data)

truth.cp4.data = truthCalc("TSK.PRB.CP4.OT2.001.1ST.", "TSK.PRB.ANS.CP4.OT2.001.1ST.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
truth.cp4.data = truthCalc("TSK.PRB.CP4.OT2.001.2ND.", "TSK.PRB.ANS.CP4.OT2.001.2ND.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
truth.cp4.data = truthCalc("TSK.PRB.CP4.OT2.002.", "TSK.PRB.ANS.CP4.OT2.002.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
truth.cp4.data = truthCalc("TSK.PRB.CP4.OT2.003.", "TSK.PRB.ANS.CP4.OT2.003.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
#truth.cp4.data = truthCalc("TSK.PRB.CP4.OT2.004.", "TSK.PRB.ANS.CP4.OT2.004.", OTdataRaw.CP4, codebook.items, truth.cp4.data)
#truth.cp4.data = truthCalc("TSK.PRB.CP4.OT2.005.", "TSK.PRB.ANS.CP4.OT2.005.", OTdataRaw.CP4, codebook.items, truth.cp4.data)

#write.csv(truth.cp1.data, file = "CP1_Truthv3_Check.csv", row.names=FALSE) # write out the data

#------------------------------------------------------------------------------
# CP5. Population Movements for NEON (NYC Only)
#------------------------------------------------------------------------------

truth.cp5.data = truthCalc("TSK.PRB.CP5.OT1.001.", "TSK.PRB.ANS.CP5.OT1.001.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT1.002.", "TSK.PRB.ANS.CP5.OT1.002.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT1.003.", "TSK.PRB.ANS.CP5.OT1.003.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT1.004.", "TSK.PRB.ANS.CP5.OT1.004.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
#truth.cp5.data = truthCalc("TSK.PRB.CP5.OT1.005.", "TSK.PRB.ANS.CP5.OT1.005.", OTdataRaw.CP5, codebook.items, truth.cp5.data)

truth.cp5.data = truthCalc("TSK.PRB.CP5.OT2.001.", "TSK.PRB.ANS.CP5.OT2.001.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT2.002.", "TSK.PRB.ANS.CP5.OT2.002.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT2.003.", "TSK.PRB.ANS.CP5.OT2.003.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT2.004.", "TSK.PRB.ANS.CP5.OT2.004.", OTdataRaw.CP5, codebook.items, truth.cp5.data)
truth.cp5.data = truthCalc("TSK.PRB.CP5.OT2.005.", "TSK.PRB.ANS.CP5.OT2.005.", OTdataRaw.CP5, codebook.items, truth.cp5.data)

#write.csv(truth.cp1.data, file = "CP1_Truthv3_Check.csv", row.names=FALSE) # write out the data

#-------------------------------------------------------------------------------
#Merge Operations across new Data Frames
#-------------------------------------------------------------------------------

truth.cp1.data <- subset(truth.cp1.data, is.na(truth.cp1.data[,"SYS.IND.SESS."])==FALSE)
truth.cp2.data <- subset(truth.cp2.data, is.na(truth.cp2.data[,"SYS.IND.SESS."])==FALSE)
truth.cp3.data.agg <- subset(truth.cp3.data.agg, is.na(truth.cp3.data.agg[,"SYS.IND.SESS."])==FALSE)
truth.cp4.data <- subset(truth.cp4.data, is.na(truth.cp4.data[,"SYS.IND.SESS."])==FALSE)
truth.cp5.data <- subset(truth.cp5.data, is.na(truth.cp5.data[,"SYS.IND.SESS."])==FALSE)

CP.truth.data =list(truth.cp1.data,truth.cp2.data,truth.cp3.data.agg,truth.cp4.data,truth.cp5.data) #add truthed dataframes to single list
CP.truth.data.merged = Reduce(function(...) merge(..., by = "SYS.IND.SESS.",all.y = TRUE), CP.truth.data) #simultaneously merge all dataframes indexed by case identifier

#Merge with Raw Data

mongo.data.truthed <- merge(raw.data,CP.truth.data.merged,by= "SYS.IND.SESS.", all =TRUE)

# merge with old User-Ale log data
# comment out if no longer needed
xdatalog.data <- read.csv("xdatatimelog.csv", header=TRUE, stringsAsFactors=FALSE)
colnames(xdatalog.data)[colnames(xdatalog.data)=="sessionID"] <- "SYS.IND.SESS."
xdatalog.data<-xdatalog.data[!duplicated(xdatalog.data["SYS.IND.SESS."]),] #remove dupe cases by SESS ID
mongo.data.truthed <- merge(mongo.data.truthed,xdatalog.data,by= "SYS.IND.SESS.", all.x =TRUE)
mongo.data.truthed["SYS.FIL.STD."][is.na(mongo.data.truthed["SYS.FIL.STD."])] <- as.character(mongo.data.truthed["timestamp"][is.na(mongo.data.truthed["SYS.FIL.STD."])])

# save the raw plus truthed data

#write.csv(mongo.data.truthed, file = "mongo.data.truthed.csv", row.names=FALSE)

#--------------------------------------------------------------------------------------------------------------

#Temporal Variables Computation; Authors: Joshua C. Poore, Eric M. Jones. 
#This script ingests stout start time output, adjusts time synchronization between STOUT and other procs and prepares it for additional processing within R

#v1 Eric Jones: 
#v2 Joshua Poore: Updated data handling, subsetting based on varname parsing. Generalized code to work for numerous variables, rather than 2.
#v3 Joshua Poore, Fei Sun: Updated Sync Operations to include data from STOUT-USER ALE for timing params. Updated data handling for fewer loops.

#Dependencies
##Paste Index Fucntion
Paste.Index = function(text.name, index){ #this function pastes a new index term to a text value. Inputs = text.name (value I want to print to), index (new index I want to print onto name)
  paste(text.name,index, sep = "", collapse = "")
}

##Time Extract Function
# 2015-12-28 21:48:34
Time.Extract = function(time.value, timezone){ #this function strips time from a value, and formats it in POSIX time, Inputs = time.value (value I want formated), timezone (timezone of value)
  format(as.POSIXct(strptime(time.value,"%Y-%m-%d %H:%M:%S", tz = timezone)))
}
# 2016-03-26T19:31:46.562Z
Timez.Extract = function(time.value, timezone){ #this function strips time from a value, and formats it in POSIX time, Inputs = time.value (value I want formated), timezone (timezone of value)
  format(as.POSIXct(strptime(time.value,"%Y-%m-%dT%H:%M:%S", tz = timezone)))
}

Sync.Conversion = function(time.value, sync.delta.time, timezone){
  format(as.POSIXct(time.value, tz = timezone) - sync.delta.time)
}

client.tz = "utc"
surveymonkey.tz = "utc"

#Data Ingest
#Create new dataframe with index values (SessID and STOUT Session Time) and times for converstion
time.data<- cbind(subset(mongo.data.truthed, select = c(SYS.IND.SESS.,SYS.FIL.STD.)),subset(mongo.data.truthed, select = (grepl("TSK.FIL.STD.",names(raw.data)) | (grepl("TSK.FIL.END.",names(raw.data)) ==TRUE)))) #subset and bind dataframe together
colnames(time.data)[3:ncol(time.data)] <- sapply(colnames(time.data)[3:ncol(time.data)],Paste.Index, "CORR.") #apply new index on colnames

time.data[,3:ncol(time.data)] = sapply(time.data[,3:ncol(time.data)],Time.Extract, surveymonkey.tz) #reformat into POSIX time format (gmt)
time.data[,"SYS.FIL.STD."] = sapply(time.data[,"SYS.FIL.STD."],Timez.Extract, client.tz) #reformat STOUT Session time

for (i in 1:nrow(time.data)){
  times.order<-order(time.data[i,3:ncol(time.data)],decreasing = FALSE, na.last = NA) #find the "start date" for non-client times (e.g., forms), should be first for each session

  # for missing time data, not able to sort, times.order=length(0)
  if(length(times.order)<=0) {
    times.order<-c(1);
  }

  sync.diff<- as.numeric(difftime(time.data[i,"SYS.FIL.STD."],time.data[i,2+(times.order[1])], units="secs")) #calculate the difference in time by subtracting non-client "start date" from client start date (SYS.FIL.STD.) 
  time.data[i,3:ncol(time.data)] = sapply(time.data[i,3:ncol(time.data)],Sync.Conversion, sync.diff, client.tz) #substracts the sync difference from each value in times.to.sync, prints new values over old.
}

#Computes delta between end and start times.
#new data frame from END times, start times will be subtracted from these values. *MOVE TO SAPPLY LATER
time.data.delta <- cbind(subset(time.data, select= c(SYS.IND.SESS.,SYS.FIL.STD.)), subset(time.data, select = (grepl("TSK.FIL.END.",names(time.data))==TRUE)))
for (i in 3:ncol(time.data.delta)){ #Assign new column names to the new data frame to dindicate they are deltas
  colnames(time.data.delta)[i] <- paste("TSK.TIME.DIFF.",substr(colnames(time.data.delta[i]),start=13,stop=24), sep = "", collapse = "")
}

for(j in names(time.data.delta)[3:ncol(time.data.delta)]){
  #if(is.na(time.data.delta[,j])==FALSE){
  x = time.data[,paste("TSK.FIL.STD.",substr(colnames(time.data.delta[j]),start=15,stop=29),"CORR.",sep = "", collapse = "")]
  y = time.data.delta[,j]
  time.data.delta[,j] = as.numeric(difftime(y,x,units="secs"))
}

#merge data files and write out
colnames(mongo.data.truthed)[colnames(mongo.data.truthed)=="SYS.FIL.STD."] <- "SYS.FIL.STD.UTC."
time.data.delta <- subset(time.data.delta, select=-c(SYS.FIL.STD.))
working.truthed.timed.data = list(mongo.data.truthed,time.data,time.data.delta) #add truthed dataframes to single list
working.truthed.timed.data = Reduce(function(...) merge(..., by = "SYS.IND.SESS."), working.truthed.timed.data)
working.truthed.timed.data <- as.data.frame(working.truthed.timed.data, stringsAsFactors = FALSE)

#write.csv(working.truthed.timed.data, file = "working.truthed.timed.data.csv", row.names=FALSE)

#______________________________________________________________________________________________________________
#SCO+CH

#Scale Computation Operations + Codebook Handling (SCO+CH); Authors:Joshua C. Poore, Eric M. Jones. 
#This script produces aggregates across questionnaire data, such as scale and subscale means. Ends with reporting out descriptive statistics.

#v1 Joshua Poore: Core data ingest, variable substring decomposition, variable substring matching, core means loop, output bind to dataframes, write out functions, documentation 
#v2 Eric Jones:   Created dataPull() function, wrote reverse scoring code, incorporated dataPull() function in code to calcualte scale and ...
#                 subscale means, wrote code to make sure no redundant columns are appended to the intake data, documentation
#v3 Joshua Poore: Added row indexing for easy reference by PID & Variable, removed dataPull function in favor of base R subsetting functions;
#                 added codebook ingest and output to reverse coding code and weighting; additional loop for computing scales from subscales; documentation
#v5 Eric Jones:   wrote and tested Reverse Coding, Weighting, and Aggregated Means functions
#v6 Joshua Poore: Integrated sequential aggregation, "saverage,ssum" operation functionality. Revised object naming conventions for clarity.
#Dependencies: coefficientalpha(resm,lavaan),xlsx(rJava,xlsxjars),write.xls{xlsReadWrite},gdata


#--------------------------------------------------------------------------------------------------------------
# Reverse Coding Function
# if a variable is flagged for reverse scoring (as indicated in the codebook), reverse the scores, replacing the values in the column
# Arguments:
    # data - dataframe of raw (all) data
    # metadata - dataframe of codebook data
    # revCodeName - name of the column in the codebook that flags a variable for reverse coding
    # scaleMaxName - name of the column in the codebook that holds the maximum scale value for each variable

reverseCode = function(data, metadata, varCol, revCol, scaleMaxCol){
row.names(metadata) <- make.names(metadata[,varCol], unique=TRUE)
  
  for(j in names(data)){                           # for each column [j], i.e., for each variable
    if(!is.na(metadata[j, revCol])){   # only if the reverse code designation cell is not blank
      if(metadata[j, revCol] == 1){    # if the variable is designated for reverse coding
        for(i in 1:nrow(data)){                     # for all elements in each row within the column
          if(!is.na(data[i,j])){                    # but only if the elements are not missing        
            data[i,j] = as.numeric(metadata[j, scaleMaxCol]) + 1 - as.numeric(data[i,j]) # reverse code by subtracting raw value from 1 + the scale maximum
          }
        }
      }
    }
  }
  
  #return the modified set of data
  reverseCode = data
}


#--------------------------------------------------------------------------------------------------------------
# Weighting Function
# if a variable is flagged for weighting (as indicated in the codebook), multiply the value by the weight
# Arguments:
    # data - dataframe of raw (all) data
    # metadata - dataframe of codebook data
    # wtName - name of the column in the codebook that holds the weighting value for each variable

weighting = function(data, metadata, varCol, wtCol){
row.names(metadata) <- make.names(metadata[,varCol], unique=TRUE)
  
  for(j in names(data)){                          # for each column [j], i.e., for each variable
    if(!is.na(metadata[j, wtCol])){    # but only for weights that are not missing
      for(i in 1:nrow(data)){                       # for all elements in each row within the column
        if(!is.na(data[i,j])){                      # but only if the elements are not missing
          data[i,j] = as.numeric(data[i,j])*as.numeric(metadata[j, wtCol]) # weight the item by multiplying it by the weight
        }
      }
    }
  }
  
  #return the modified set of data
  weighting = data
}


#--------------------------------------------------------------------------------------------------------------
# Scale Computation Function
# Based on index terms embedded in variable names in a codebook, function will extract the correct data, and aggregate them appropriately.
# Arguments:
    # data - dataframe of raw (all) data
    # varIndices - a list containing an indeterminate number of indices, separated by a delimiter, that are contained in all the variables across which we want to calculate a mean
    # opNames - name of the column in the codebook that holds the operation to be performed for each variable
    # checkMat - returns a matrix of booleans indicated which variable in the raw dataset were included for aggregation

calcScales = function(data, varIndices, opNames, checkMat){

# initialize dataframes to hold the data the data to aggregate and the aggregates
VarsToAgg = data.frame(matrix(0, nrow(data),1)) # variables extracted for aggregation
ScaleAgg = data.frame(matrix(0, nrow(data),1)) # aggregated variables


#create a flag to check if the variable name contains all the desired descriptors, and should be selected for aggregation.
VarIndCheck = TRUE

for (col in 1:ncol(data)){          # for all the columns in the data matrix
  for(m in 1:length(varIndices)){    # for all the descriptors that I wish to match
    
    # if I previously determined that a desciptor is not in the variable name, or if the current descriptor is not in the variable name 
    if(VarIndCheck == FALSE | grepl(varIndices[m], names(data[col])) == FALSE){ 
      VarIndCheck = FALSE   # set my flag to false because the variable does not meet my criteria
    }
  }
  
  if(VarIndCheck == TRUE){   # if my flag is true, meaning the variable does meet my criteria
    VarsToAgg=cbind(VarsToAgg,data[,col])                   # extract relevant data columns pull the data from that column and put in the new matrix
    names(VarsToAgg)[ncol(VarsToAgg)] = names(data)[col]    # change the name of that new column
    
    checkMat[paste(varIndices, sep="", collapse = ""), names(data)[col]] = checkMat[paste(varIndices, sep="", collapse = ""), names(data)[col]] + 1 
    
  }
  # reset the flag for the next variable
  VarIndCheck = TRUE
}
   
  if(ncol(VarsToAgg) >= 3){                             # if more than 2 columns of data are pulled 
    VarsToAgg = VarsToAgg[,2:ncol(VarsToAgg)]   # remove the column of zeroes that was created when initializing the temporary dataframe
    if(opNames == "average"){
      ScaleAgg = rowMeans(VarsToAgg, na.rm = TRUE)        # calculate the row means and append the column of means to the raw data file
    }
    else if(opNames == "sum"){
      ScaleAgg = rowSums(VarsToAgg, na.rm = TRUE)        # calculate the row means and append the column of means to the raw data file
    }  
    else if(opNames == "saverage"){
      ScaleIndexLength <- length(gregexpr("\\.", paste(varIndices,sep='',collapse=''))[[1]]) #find the number of indices in the scale variable (to compute) by index delimiter (".") 
      AggIndices <- rev(1:max(unlist(lapply(gregexpr("\\.",names(VarsToAgg)),length)))) #find the number of indices in the strings of variables selected to aggregate as array      
      for (i in AggIndices){
        if(i == max(AggIndices)){ # if this is the first step of aggregation (Step1) 
          SortAggVars <- as.data.frame(sort(names(VarsToAgg)), stringsToFactors = FALSE) #sort subset of vars to aggregate by name, ascending, coerce to dataframe for reference
          CommonVarInd <-substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[",i-1)) #extract common strings amongst variable selections
          SubsetIndToAgg <-subset(CommonVarInd,duplicated(substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[", i-1)))==FALSE) #remove duplicates from CommonVarInd
          ScaleAggStep <- data.frame(matrix(0, nrow(data), ncol = length(SubsetIndToAgg))) #initialize dataframe for step-wise aggregates
          names(ScaleAggStep) <- SubsetIndToAgg[1:length(SubsetIndToAgg)] #give names to dataframe columns for step-wise aggregates
          for(k in 1:length(SubsetIndToAgg)){ # for each element in subset array of indices for step 1 aggregation  
            VarsAggStep <- subset(data, select = (grepl(SubsetIndToAgg[k], names(data))==TRUE)) # raw data variables names subset from Step 1 aggregation vars
            AggStep <- as.data.frame(rowMeans(VarsAggStep, na.rm = TRUE), stringsAsFactors=FALSE) #format averages from RowMeans across Step 1[1] vars into new column
            names(AggStep) = SubsetIndToAgg[k]
            ScaleAggStep[,names(AggStep)]<-AggStep
          }
        }  
        else if(i < max(AggIndices) & i > ScaleIndexLength + 1){
          SortAggVars <- as.data.frame(sort(names(ScaleAggStep)), stringsToFactors = FALSE) #sort subset of vars to aggregate by name, ascending, coerce to dataframe for reference
          CommonVarInd <-substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[",i-1)) #extract common strings amongst Step 1 selections
          SubsetIndToAgg <-subset(CommonVarInd,duplicated(substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[", i-1)))==FALSE) #remove duplicates from CommonVarInd
          for(k in 1:length(SubsetIndToAgg)){ # for each element in subset array of indices for step n aggregation  
            VarsAggStep <- subset(ScaleAggStep, select = (grepl(SubsetIndToAgg[k], names(ScaleAggStep))==TRUE)) # raw data variables names subset from Step 1 aggregation vars
            AggStep <- as.data.frame(rowMeans(VarsAggStep, na.rm = TRUE), stringsAsFactors=FALSE) #format averages from RowMeans across Step 1[1] vars into new column
            names(AggStep) = SubsetIndToAgg[k]
            ScaleAggStep[,names(AggStep)]<-AggStep
          }
        }
        else if(i == ScaleIndexLength + 1){
          SortAggVars <- as.data.frame(sort(names(ScaleAggStep)), stringsToFactors = FALSE) #sort subset of vars to aggregate by name, ascending, coerce to working.proc.dataframe for reference
          CommonVarInd <-substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[",i)) #extract common strings amongst Step 1 selections
          SubsetIndToAgg <-subset(CommonVarInd,duplicated(substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[", i)))==FALSE) #remove duplicates from CommonVarInd
          VarsAggStep <- subset(ScaleAggStep, select = names(ScaleAggStep) %in% SubsetIndToAgg) # raw working.proc.data variables names subset from Step 1 aggregation vars
          AggStep <- as.data.frame(rowMeans(VarsAggStep, na.rm = TRUE), stringsAsFactors=FALSE) #format averages from RowMeans across Step 1[1] vars into new column
          names(AggStep) = paste(varIndices,sep='',collapse='')
          ScaleAggStep[,names(AggStep)]<-AggStep
          }
        else if(i == ScaleIndexLength | i < ScaleIndexLength){
        ScaleAgg = ScaleAggStep[,paste(varIndices,sep='',collapse='')]
        #write.csv(ScaleAggStep,paste("saverage_",paste(varIndices,sep='',collapse=''),".csv",sep='',collapse=''), append = TRUE)
        }
      }
    }
    else if(opNames == "ssum"){
    ScaleIndexLength <- length(gregexpr("\\.", paste(varIndices,sep='',collapse=''))[[1]]) #find the number of indices in the scale variable (to compute) by index delimiter (".") 
    AggIndices <- rev(1:max(unlist(lapply(gregexpr("\\.",names(VarsToAgg)),length)))) #find the number of indices in the strings of variables selected to aggregate as array      
     for (i in AggIndices){
        if(i == max(AggIndices)){ # if this is the first step of aggregation  
          SortAggVars <- as.data.frame(sort(names(VarsToAgg)), stringsToFactors = FALSE) #sort subset of vars to aggregate by name, ascending, coerce to dataframe for reference
          CommonVarInd <-substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[",i-1)) #extract common strings amongst variable selections
          SubsetIndToAgg <-subset(CommonVarInd,duplicated(substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[", i-1)))==FALSE) #remove duplicates from CommonVarInd
          ScaleAggStep <- data.frame(matrix(0, nrow(data), ncol = length(SubsetIndToAgg))) #initialize dataframe for 
          names(ScaleAggStep) <- SubsetIndToAgg[1:length(SubsetIndToAgg)]
          for(k in 1:length(SubsetIndToAgg)){ # for each element in subset array of indices for step 1 aggregation  
            VarsAggStep <- subset(data, select = (grepl(SubsetIndToAgg[k], names(data))==TRUE)) # raw data variables names subset from Step 1 aggregation vars
            AggStep <- as.data.frame(rowSums(VarsAggStep, na.rm = TRUE), stringsAsFactors=FALSE) #format averages from RowMeans across Step 1[1] vars into new column
            names(AggStep) = SubsetIndToAgg[k]
            ScaleAggStep[,names(AggStep)]<-AggStep
          }
        }
        else if(i < max(AggIndices) & i > ScaleIndexLength +1 ){
          SortAggVars <- as.data.frame(sort(names(ScaleAggStep)), stringsToFactors = FALSE) #sort subset of vars to aggregate by name, ascending, coerce to dataframe for reference
          CommonVarInd <-substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[",i-1)) #extract common strings amongst Step 1 selections
          SubsetIndToAgg <-subset(CommonVarInd,duplicated(substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[", i-1)))==FALSE) #remove duplicates from CommonVarInd
          for(k in 1:length(SubsetIndToAgg)){ # for each element in subset array of indices for step 1 aggregation  
            VarsAggStep <- subset(ScaleAggStep, select = (grepl(SubsetIndToAgg[k], names(ScaleAggStep))==TRUE)) # raw data variables names subset from Step 1 aggregation vars
            AggStep <- as.data.frame(rowSums(VarsAggStep, na.rm = TRUE), stringsAsFactors=FALSE) #format averages from RowMeans across Step 1[1] vars into new column
            names(AggStep) = SubsetIndToAgg[k]
            ScaleAggStep[,names(AggStep)]<-AggStep
          }
        }
        else if(i == ScaleIndexLength + 1){
          SortAggVars <- as.data.frame(sort(names(ScaleAggStep)), stringsToFactors = FALSE) #sort subset of vars to aggregate by name, ascending, coerce to working.proc.dataframe for reference
          CommonVarInd <-substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[",i)) #extract common strings amongst Step 1 selections
          SubsetIndToAgg <-subset(CommonVarInd,duplicated(substr(SortAggVars[,1],start=1,stop=sapply(gregexpr("\\.",SortAggVars[,1]),"[[", i)))==FALSE) #remove duplicates from CommonVarInd
          VarsAggStep <- subset(ScaleAggStep, select = names(ScaleAggStep) %in% SubsetIndToAgg) # raw working.proc.data variables names subset from Step 1 aggregation vars
          AggStep <- as.data.frame(rowSums(VarsAggStep, na.rm = TRUE), stringsAsFactors=FALSE) #format averages from RowMeans across Step 1[1] vars into new column
          names(AggStep) = paste(varIndices,sep='',collapse='')
          ScaleAggStep[,names(AggStep)]<-AggStep
          }
        else if(i == ScaleIndexLength | i < ScaleIndexLength){
        ScaleAgg = ScaleAggStep[,paste(varIndices,sep='',collapse='')]
        #write.csv(ScaleAggStep,paste("saverage_",paste(varIndices,sep='',collapse=''),".csv",sep='',collapse=''), append = TRUE)
        }
      }
    }
  else if(ncol(VarsToAgg) == 2){     # if only 1 column of data is pulled
      ScaleAgg = VarsToAgg[,2]    # append that column of data to the raw data file
    }  
  }
  calcScales = list(ScaleAgg, checkMat)
}


#--------------------------------------------------------------------------------------------------------------
# Reverse Code - Function Call
working.truthed.timed.data = reverseCode(working.truthed.timed.data, codebook.items, "varnames", "reverse.code", "scale.max")

#--------------------------------------------------------------------------------------------------------------
# Item Weighting - Function Call
working.truthed.timed.data = weighting(working.truthed.timed.data, codebook.items, "varnames", "weight")

#--------------------------------------------------------------------------------------------------------------
# Aggregated Means Using Codebook

working.proc.data.scale = working.truthed.timed.data    # create a new dataframe which will hold the means
varIndices = list()          # initialize a list containing the descriptors that will be found

aggCheck = matrix(0, length(codebook.scales[,1]), length(names(working.truthed.timed.data)))
rownames(aggCheck) = codebook.scales[,1]
colnames(aggCheck) = names(working.truthed.timed.data)


for(k in 1:nrow(codebook.scales)){    # for all the variables in the codebook
  if ((codebook.scales[k,1] %in% names(working.truthed.timed.data )) == FALSE ){    # if the variable is not in the dataset, we need to calculate the means and append the column
    
    delimiter = gregexpr("\\.", codebook.scales[k,1])                 # determine the locations of all the delimiters (periods)
    
    for(p in 1:length(delimiter[[1]])){   # for as many indices as there are in the variable name
      if(p == 1){                       # special case when pulling out the first descriptor
        varIndices = c(varIndices, substr(codebook.scales[k,1],start=1,stop=delimiter[[1]][[p]]))   # code for pulling out the decriptor and adding to the list
      }
      else{
        varIndices = c(varIndices, substr(codebook.scales[k,1],start=delimiter[[1]][[p-1]]+1,stop=delimiter[[1]][[p]]))   # code for pulling out the decriptor and adding to the list
      }
    }
    
    listReturn = calcScales(working.truthed.timed.data, varIndices, codebook.scales[k, "operation"], aggCheck)
    
    # calculate the mean of the new variable, and append to the working dataset
    working.proc.data.scale = cbind(working.proc.data.scale, listReturn[[1]])
    names(working.proc.data.scale)[ncol(working.proc.data.scale)] = codebook.scales[k,1]     # change the name of the column
    
    aggCheck = listReturn[[2]]
    
    # reset the list that contains the indices
    varIndices = list()
    
  }
}

write.csv(working.proc.data.scale, file = matFile, row.names=FALSE)
write.csv(working.proc.data.scale, file="MasterAnswerTable.csv", row.names=FALSE)

#write.csv(aggCheck, file = paste(Sys.time(),"aggCheck.csv",sep = "_", collapse=""))
#write.csv(aggCheck, file = "aggCheck.csv", collapse="")
write.csv(aggCheck, file = aggCheckFile)

# Save a simple version in JSON format for D3 histogram
library(rjson)
histData <- working.proc.data.scale[,c("SYS.FIL.APP.","SYS.FIL.TSK.","PST.EXP.CLD.","PST.EXP.BED.","TSK.PRB.ANS.","TSK.CON.","TSK.TIME.DIFF.")]
sink("2015_public_xdataonline.json")
cat( toJSON(unname(split(histData, 1:nrow(histData)))) )
sink()

