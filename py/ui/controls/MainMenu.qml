import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    id: mainMenu

    component Title: Text {
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 32
        color: "white"
    }
    component TitleButton: Button {
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 32
    }
	
	
    Image {
        id: image
        anchors.fill: parent
        source: "qrc:/bg"
        fillMode: Image.PreserveAspectCrop
    }

    Item {
        anchors.fill: parent
        anchors.centerIn: parent
    
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: parent.height * .2
        anchors.bottomMargin: parent.height * .4
        z: 3
    
        Rectangle {
            anchors.fill: parent
            opacity: .5
            color: "#222222"
        }
    
        Column {
            anchors.centerIn: parent
            anchors.leftMargin: 100
            anchors.rightMargin: 100
            anchors.topMargin: 100
            anchors.bottomMargin: 100
            z: 4
    
            Image {
                id: logo
                source: "qrc:/logo"
                width: 300
                sourceSize.width: width*10
                fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter
                mipmap: true
                smooth: true
                z: 5 // over everything
                            
                SequentialAnimation {
                    running: mainMenu.visible
                    ScaleAnimator {
                        duration: 500; target: logo
                        from: 20.0; to: 1.2
                        easing.type: Easing.InQuad;//Elastic;
                    }
                    ScaleAnimator {
                        duration: 500; target: logo
                        from: 1.2; to: 1.0
                        easing.type: Easing.InQuad;                 
                    }
                }
            }    
            Title {
                id: title
                font.pixelSize: 64
                text: "Music Experiment Game"
            }
            Title {
                id: statusLine0
                text: " "
            }
            
        }
    }
        
    Column {
        z: 2
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 100
        
        TitleButton {
            text: "New Game"
            onClicked: {
                backend.newGame()
            }
        }
        Title {
            text: "~"
        }
        TitleButton {
            text: "Play MIDIs"
            onClicked: {
                backend.playMidis()
            }
        }
    }
    GamesByLogo {
        z: 1
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }
}