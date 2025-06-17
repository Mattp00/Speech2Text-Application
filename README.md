# Speech2Text-Application

## Introduction
The speech to text application was created for a project workshop during my university studies with an external IT company. 
The first part of the project involved a review of the literature on this specific case, the main paid services (using APIs), and the available open-source models.

The models have been primarily tested in Italian, but they are capable of recognizing multiple languages.
In the evaluation phase, 3 out of 4 datasets are in Italian, and only 1 is in English.

## Fine-tune and Evaluation
Subsequently, the notebook defines a script to fine-tune and evaluate some of the best open-source speech-to-text models.
The implemented dataset are:
1) Italic
2) Common-Voice
3) Minds14
4) AMI (english only)

The tested models are:
1) Whisper (base-medium-large) and other finetuned versions;
2) SeamlessM4T2

The considered metrics are:
1) WER (Word Error Rate)
2) CER (Character Error Rate)
3) Inference time

The following metrics refer only to the first 1,500 rows of the test set.
![wer](https://github.com/user-attachments/assets/6ad1ecac-5fda-4249-a7ff-c984cdd8d8c8)

![cer](https://github.com/user-attachments/assets/ddc727ae-598a-44fb-84a2-85dd6ab0327c)

![inference_time](https://github.com/user-attachments/assets/ee400716-4ebc-41e1-8fa6-41309c96eefd)



## Implementation of a speech2text application using a client-server architecture

The implementation of a speech-to-text application required the use of the following frameworks:

1) Flask: a Python-based backend framework

2) Flutter: a DART (C++ based) frontend framework

The Flask backend use a fine-tuned version of the Whisper automatic speech recognition model.

The frontend is a simple application that allows you to record and load an audio track using your microphone, and then send it to the server with a button.
If the application doesn't start when clicking the "Start" button, you can run it manually by typing flutter run in your console and selecting a browser (I tested it using Google Chrome).
