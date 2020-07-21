# social_distancingAPP
Social Distancing app made using tiny yolov4 <br/>
![alt_text](https://github.com/pritul2/social_distancingAPP/blob/master/convert-to-giff.gif)

# Installing libraries for GPU/CPU
1. Inside Terminal or Command Prompt write
```
git clone https://github.com/AlexeyAB/darknet
pip install opencv-contrib-python
```
2. replace the Makefile in cloned directory with Makefile from my GPU folder if using GPU else from CPU folder<br/>
3. Inside Terminal or Command Prompt write
```
make
```
4. Download weights from here
https://github-production-release-asset-2e65be.s3.amazonaws.com/75388965/bc496b80-b701-11ea-817e-8c227b647432?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20200721%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20200721T120552Z&X-Amz-Expires=300&X-Amz-Signature=782eee329a726b51d3ad266fc3bf42ff0f8b5de4d629eaaf1d7185a44fb00910&X-Amz-SignedHeaders=host&actor_id=41751718&repo_id=75388965&response-content-disposition=attachment%3B%20filename%3Dyolov4-tiny.weights&response-content-type=application%2Foctet-stream
5. Clone my repository
```
git clone https://github.com/pritul2/social_distancingAPP
```
6. Copy and replace all files from social_distancingAPP to darknet folder

For any more errors in installing check on issue section of AlexyAb </br>
https://github.com/AlexeyAB/darknet/issues
