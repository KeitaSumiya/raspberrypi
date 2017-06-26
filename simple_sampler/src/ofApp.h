#pragma once

#include "ofMain.h"
#include "ofxGPIO.h"

class ofApp : public ofBaseApp{

	public:
    void setup();
    void update();
    void draw();
 
    void keyPressed(int key);
    void keyReleased(int key);
    void mouseMoved(int x, int y );
    void mouseDragged(int x, int y, int button);
    void mousePressed(int x, int y, int button);
    void mouseReleased(int x, int y, int button);
    void mouseEntered(int x, int y);
    void mouseExited(int x, int y);
    void windowResized(int w, int h);
    void dragEvent(ofDragInfo dragInfo);
    void gotMessage(ofMessage msg);
    void audioIn(float * input, int bufferSize, int nChannels);
    void audioOut(float * output, int bufferSize, int nChannels);
    
    static const int SampleRate = 48000;
    static const int BufferSizeMax = SampleRate * 5;

    ofRtAudioSoundStream soundStream;
    float buffer[BufferSizeMax];
    int recPos;
    int recSize;
    int playPos;
    int mode; //0:off, 1:recording, 2:play
    GPIO gpioR;
    string state_buttonR;
    GPIO gpioP;
    string state_buttonP;
    GPIO gpioB;
    string state_buttonB;
};
