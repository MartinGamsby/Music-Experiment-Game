import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material


AnimatedImage {
    property bool loop: true
    
    fillMode: Image.PreserveAspectCrop
    width: 300
    height: width/2
    source: "qrc:/GamesByGamsby.gif"
    playing: visible
    onFrameChanged: {
        if(!loop && currentFrame==(frameCount-1)) {
            playing = false
            //currentFrame = 25
        }
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            Qt.openUrlExternally("http://linktr.ee/Gamsby")
        }
    }
}