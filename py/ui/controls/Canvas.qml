import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Rectangle {
    color: "black"
    
    component Title: Text {
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 60
        color: "white"
    }
    
    Title {            
        anchors.centerIn: parent
        text: model ? model.p_title : ""
    }
    Title {
        font.pointSize: 40
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 9
        anchors.bottomMargin: 19
    
        text: model ? model.p_music_state_pretty_name : ""        
    }
    Rectangle {
        color: "white"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 0
        height: 10
        width: model ? (model.p_music_progress * parent.width) : 0
    }
    
}
