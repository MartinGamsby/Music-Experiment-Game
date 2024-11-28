import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import QtQuick.Dialogs

// For State and MusicState enums
import com.martingamsby.music 1.0

ColumnLayout {
    id: musicSettingsRoot
    
    component IdeaSetting: SettingBool {
        
        anchors.margins: 24
        
        property Item under: null
        property Item rightOf: null
        
        // already checked: can uncheck.
        // otherwise only enabled if we have enough remaining ideas
        enabled: (setting ? setting.b : false) || (model ? ((model.p_total_ideas.i - model.p_ideas.i)>0) : false)
        alignCenter: true
        
        anchors.top: under ? under.bottom : undefined
        x: under ? under.x : 0
        
        y: rightOf ? rightOf.y : 0
        
        anchors.left: rightOf ? rightOf.right : undefined
    }
    
    Title {
        Layout.fillWidth: true
        
        Layout.margins: 18
        
        color: enabled ? Material.foreground : Material.hintTextColor
        text: tr("MUSIC_SETTINGS")
    }
    
    Rectangle {
        property int margin: 2
        width: flickable.width + margin*2
        height: flickable.height + margin*2
        border.color: "#222222"
        border.width: margin
        color: "transparent"
        radius: 9
        
        Flickable {
            id: flickable
            width: 360 
            height: 360
            contentWidth: contents.width
            contentHeight: contents.height
            anchors.centerIn: parent
            clip: true

            ScrollBar.vertical: ScrollBar {
                width: 40
                anchors.left: parent.right // adjust the anchor as suggested by derM
                policy: ScrollBar.AlwaysOn
            }
            Rectangle {
                id: contents
                color: Qt.rgba(0,0,0,0.25)
                radius: 9
                
                height: 500
                width: 500
                
                IdeaSetting {
                    id: baseSetting
                    anchors.centerIn: parent
                    
                    setting: model ? model.p_frequency : null
                }
                IdeaSetting {
                    id: setting2 // TODO: Use yaml?
                    
                    under: baseSetting
                    setting: model ? model.p_instruments : null
                }
                IdeaSetting {
                    setting: model ? model.p_instrument_piano : null
                    rightOf: setting2
                }
            }
            Component.onCompleted: {
                flickable.contentY = flickable.contentHeight / 2 - height / 2
                flickable.contentX = flickable.contentWidth / 2 - width / 2
            }
        }
    }
    Button {
        text: tr("MAKE_ANOTHER_MUSIC")
        Layout.margins: 9
        
        onClicked: {
            backend.makeAnotherMusic()
        }
    }
    Item {
        Layout.fillHeight: true
    }
}
