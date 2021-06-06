# pose_cnn_workout_assistance

This is a workout assistant that can count the reps of workouts in realtime using pose-estimation.  

* A convolutional neural network is trained on pose data of a selected exercise (shoulder dumbbell press) in it's various states. 
* Pose data is generated from live webcam feed 
* Classification is performed on it to classify it into one of the several states of an exercise. 
* Based on this classification, reps are counted.  

The user can view the results in a web app.

### Timeline

This project is currently a WIP. I am working along the following timeline:

* [x] Get train/test images
* [x] Write tools for automated pose-detection in input images
* [x] Train a CNN model with acceptable loss on pose data
* [x] Do local evaluations, re-trainings
* [x] Save model in tensorflow.js format
* [ ] Make web app
* [ ] Deploy app
