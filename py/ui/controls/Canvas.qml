import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Rectangle {
    color: "#666"
    
    component Title: Text {
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 60
        color: "white"
    }
    
    Title {            
        anchors.centerIn: parent
        text: "Canvas"
    }
    Title {
        font.pointSize: 40
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 9
    
        text: model ? model.p_music_state_pretty_name : ""
        
    }
}
