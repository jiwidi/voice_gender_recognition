# Gender recognition from voice files

Run in online at https://hub.mybinder.org/user/jiwidi-voice_gender_recognition-bxja2kyq/tree (thx binder https://mybinder.org/, cool tech)

## Jaime Ferrando submission to Lukasz Tracewski from Sandvik CODE assigment

## Introduction

This project is my submission for the Sandvik CODE assigment.

The goal is to predict a person gender by analyzing digital samples of its voice. 

The data consisted in a series of .wav files along some logs from their extraction, I had to extract audio features from the wavs and other demographic features from the logs such as age,dialect and the target gender. All the extracting and audio processing is under the /utils/ folder at the following files:

* scraper.py, simple script to find and download all the tgz files from the provided url.
* dataset.py, Script where tgz and wavs files are explored along some extra features from the logs. This file creates a csv file containing the path for every wav file along the extra features from each of them.
* scriptR.R Parallelized R script where the warbleR library for audio processing extracts a series of audio signal features with added to the previous csv file creates the final dataset.

Here I show a brief explanation of my submission (at the jupyter notebook).


## Technologies used for this project:
*  Python
*  Sklearn
*  Pandas
*  XGBoost
*  Tensorflow
*  Bayes-opt

## Data processing

This data I obtained after processing the wav files needed some processing at:

* Removing features with >98% zeros.
* Removing features with 100% nans.
* Removing features with constant values.
* Removing duplicated features.
* Maping categorical features to reduce possible values (there was a lot of values with low number of ocurrences)
* Fix mistyped values in categorical features by mapping them.
* Transform categorical features to one-hot.

After processing the data I analyzed each feature distribution against the target variable gender, checking if it presented different distributions depending on male or female.

Correlation matrix is used to remove higly correlated features (>98%).

The dataset unbalanced respect to the target variable(82% male,18% female) so different techniques were proposed:

* SMOTE, ADASYN
* Undersampling, Oversampling
* Expand our dataset with external audio files (dataset found in kaggle)

A feature selection section is proposed, in this section join the insights from the distribution analysis with tree models to find the most important features of our model.

After all of this process 3 datasets are generated to be tested in models:

* dataframe_downsampled (processed dataset)
* dfExtra_downsampled (processed dataset + extra dataset from kaggle)
* dataframe_downsampled (processed dataset were features with more relative importance are selected)

## Training

I have tried a series of models with different hyperparameter combinations, such as:
* SVM with linear,rbf,polinomial kernels.
* Randomforest,extratrees.
* XGboost.
* DNN.

All models were tested with cross validation to ensure robust metric scores, the metric I choosed was simple accuracy as false positive and false negative had the same weight.

### Optimizing hyperparameters

After trying all the possible models and selecting the ones with best results I moved to optimize the hyperparameters of those models. This can be seen as optimizing a function whose input are the hyperparameters and whose output is the model performance measure. Optimizing this function is hard to due the following problems:
* The function is very expensive to sample because I need to train a new model each time
* We have an infinite number of possible hyperparameters 
* We do not know the interactions between these hyperparameters

To solve this problem I used Bayesian Optimization (bayes-opt package in python) for Xgboost and gridSearch for SVM.

### Final model

Our best model was XGboost with 0.891% accuracy along DNN at 0.85% and SVM at 0.82%.


## Conclusion

Now that I have finished the assgiment I want to list the most important things to do when facing a problem of this kind. Some of them were learnt during the assgiment, apart from the ones I knew beforehand:

* Perform an exhaustive study of the data distribution
* Spend time with data preprocessing, it is what usually makes the difference, as nowadays models are being easier to implement
* Distinguish between model selection and model optimization

Thanks to Sandvik CODE and Lukasz Tracewski for presenting us the assigment.
