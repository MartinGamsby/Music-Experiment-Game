import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "../controls"

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    anchors.margins: 9

    //default property alias content: contentLayout.children    
    //RowLayout {
    //    id: contentLayout
    //}
    Item {
        width: gameLogo.width/2                
    }
    TitleAnchored {
        anchors.fill:parent
        text: tr(model ? model.p_game_title.s : "")
    }
    GameLogo {
        id: gameLogo
        anchors.right: parent.right
        anchors.top: parent.top
        width: maxSizeW
        height: maxSizeH
        // TODO: Make a method, like tr() ...
        visible: model ? (model.p_gui_back_to_mainmenu.p_unlocked && model.p_gui_back_to_mainmenu.b) : false
    }
    RowLayout {
        id: ideaLayout
        visible: model ? model.p_ideas.p_unlocked : false
        GrowingImage {
            source: "qrc:/idea"
            maxSize: 40
            // TODO: checkable?
            function onClicked() {
                settingsRect.visible = !settingsRect.visible
            }
        }
        Text {
            z: 10
            text: (model ? (model.p_total_ideas.i - model.p_ideas.i) : "")
            color: enabled ? Material.foreground : Material.hintTextColor
            font.pointSize: 24
            x: 10
            //TODO: onClicked: { settingsRect.visible = !settingsRect.visible }
        }
        NumberAnimation on opacity {
            from: 0
            to: 1
            duration: 1000
            running: visible
        }
    }
    
    Rectangle {
        id: musicDescRect
        // Shown with the idea button
                
        visible: model ? (model.p_music_description.p_unlocked) : false
        
        anchors.margins: 9
        anchors.right: gameLogo.left
        x: flickable.visible ? (ideaLayout.width + 9) : (parent.width-width - 9)
        y: 9
        
        radius: 9
        color: Qt.rgba(0,0,0,0.9)
        
        width: flickable.visible ? (parent.width - ideaLayout.width - gameLogo.width - 9*4 ) : (buttonsLayout.width + 18)
        height: flickable.visible ? (parent.height*0.45) : (buttonsLayout.height + 18)
        
        ColumnLayout {
            anchors.fill: parent
            
            RowLayout {
                id: buttonsLayout
                Layout.fillWidth: true 
                Layout.margins: 9
                Layout.alignment: Qt.AlignRight                
                Title {
                    font.pixelSize: 15
                    text: tr("MUSIC_DESC_TITLE")
                }
                RoundButton {
                    text: flickable.visible ? "-" : "+"
                    font.pixelSize: 15
                    implicitWidth: 40
                    implicitHeight: 40
                    onClicked: flickable.visible = !flickable.visible
                }
            }
            
            Flickable {
                id: flickable
                
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                contentWidth: parent.width
                contentHeight: musicDescription.height + 18
                clip: true
                    
                Title {
                    id: musicDescription
                    
                    
                    font.pixelSize: 20
                    x: anchors.margins
                    y: anchors.margins
                    width: parent.width - anchors.margins*2
                    anchors.margins: 9
                    anchors.bottomMargin: 19
                    
                    wrapMode: Text.Wrap
                    textFormat: Text.RichText      
                
                    text: model ? model.p_music_detailed_desc : ""
                    horizontalAlignment: Text.AlignLeft
                }
            }
        }
    }
    Rectangle {
        id: settingsRect
        // Shown with the idea button
        
        visible: false // TODO: When making a new game, it's not hiding... use the total_ideas??
        
        anchors.top: ideaLayout.bottom
        x: 9
        radius: 9
        color: Qt.rgba(0,0,0,0.9)
        
        implicitWidth: musicSettings.width
        implicitHeight: musicSettings.height
        MusicSettings {
            id: musicSettings
        }
    }
}
