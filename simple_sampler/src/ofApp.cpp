#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    ofBackground(0);
    gpioR.setup("14");
    gpioR.export_gpio();
    gpioR.setdir_gpio("in");
    gpioP.setup("15");
    gpioP.export_gpio();
    gpioP.setdir_gpio("in");
    gpioB.setup("18");
    gpioB.export_gpio();
    gpioB.setdir_gpio("in");

    soundStream.printDeviceList();
    soundStream.setInDeviceID(0);
    soundStream.setOutDeviceID(1);
    soundStream.setup(this, 2, 1, SampleRate, BufferSizeMax, 4);
    
    mode = 0;
    
    recPos = 0;
    playPos = 0;
    recSize = 0;
}

//--------------------------------------------------------------
void ofApp::update(){
    gpioR.getval_gpio(state_buttonR);
    gpioP.getval_gpio(state_buttonP);
    gpioB.getval_gpio(state_buttonB);
    //ofLog()<<state_button;
    cout<<"R";
    cout<<state_buttonR;
    cout<<"_P";
    cout<<state_buttonP;
    cout<<"_B";
    cout<<state_buttonB<<endl;

    if(state_buttonR=="1"){
        if(mode==1){    //stop recording
            mode = 0;
            recSize = recPos;
        }else{          //start recording
            mode = 1;
            recPos = 0;
            float buffer[BufferSizeMax] = {};
        }
        playPos = 0;
        usleep(1000000);
    }else if(state_buttonP=="1"){
        if(mode==2){    //pause
            mode = 0;
        }else{          //play (in the middle)
            mode = 2;
        }
        usleep(1000000);
    }else if(state_buttonB=="1"){
        playPos = 0;    //return to the initial position
        //usleep(1000000);
    }
}

//--------------------------------------------------------------
void ofApp::draw(){
    if(mode == 0) {
        ofBackground(0);
        ofSetColor(255);
    }else if(mode == 1) {
        ofBackground(255, 0, 0);
        ofSetColor(255);
    }else if(mode == 2) {
        ofBackground(0, 0, 255);
        ofSetColor(255);
    }
    
    int ratio = BufferSizeMax / ofGetWidth();
    for (int i = 0; i < recSize; i+=ratio){
        ofDrawLine(i/ratio, ofGetHeight()/2,  i/ratio, ofGetHeight()/2+buffer[i]*500.0f);
    }
    
    if(mode==2){
        ofSetColor(0);
        for (int i = 0; i < playPos; i+=ratio){
            ofDrawLine(i/ratio, ofGetHeight()/2,  i/ratio, ofGetHeight()/2+buffer[i]*500.0f);
        }
    }
}

//--------------------------------------------------------------
void ofApp::audioIn(float * input, int bufferSize, int nChannels){
    if (mode == 1) {
        for (int i = 0; i < bufferSize*nChannels; i++){
            if(recPos<BufferSizeMax){
                buffer[recPos] = input[i];
                recPos++;
                recSize = recPos;
            } else {
                recSize = BufferSizeMax;
                mode = 0;
            }
            
        }
    }
}

void ofApp::audioOut(float *output, int bufferSize, int nChannels){
    if (mode == 2) {
        for (int i = 0; i < bufferSize; i++) {
            if(playPos<recSize){
                for(int n=0; n<nChannels; n++){
                    output[nChannels*i+n] = buffer[playPos];
                }
                playPos++;
            } else {
                mode = 0;
                playPos = 0;
            }
        }
    }
}


//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if(key=='r'){
        if(mode==1){    //stop recording
            mode = 0;
            recSize = recPos;
        }else{          //start recording
            mode = 1;
            recPos = 0;
            float buffer[BufferSizeMax] = {};
        }
        playPos = 0;
    }else if(key=='p'){
        if(mode==2){    //pause
            mode = 0;
        }else{          //play (in the middle)
            mode = 2;
        }
    }else if(key=='P'){
        playPos = 0;    //return to the initial position
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){
}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){
}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){
}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}

