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
        property Item leftOf: null
        property Item over: null
        
        // already checked: can uncheck.
        // otherwise only enabled if we have enough remaining ideas
        enabled: (setting ? setting.b : false) || (model ? ((model.p_total_ideas.i - model.p_ideas.i)>0) : false)
        alignCenter: true
        
        anchors.top: under ? under.bottom : undefined
        x: under ? under.x : (over ? over.x : 0)
        
        y: rightOf ? rightOf.y : (leftOf ? leftOf.y : 0)
        
        anchors.left: rightOf ? rightOf.right : undefined
        anchors.right: leftOf ? leftOf.left : undefined
        
        anchors.horizontalCenter: over ? over.horizontalCenter : (under ? under.horizontalCenter : undefined)
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
            width: 800 
            height: 800
            contentWidth: flickableContents.width
            contentHeight: flickableContents.height
            anchors.centerIn: parent
            clip: true

            ScrollBar.vertical: ScrollBar {
                width: 40
                anchors.left: parent.right // adjust the anchor as suggested by derM
                policy: ScrollBar.AlwaysOn
            }
            Rectangle {
                id: flickableContents
                objectName: "flickableContents"
                color: Qt.rgba(0,0,0,0.25)
                radius: 9
                
                height: 1500
                width: 1500
                
                Repeater
                {
                    id: settingRepeater
                    model: rootWindow.model ? rootWindow.model.p_music_settings : null//buildSettingsModel( musicSettings.settings )
                    
                    property var objectArray: []
    
                    delegate: 
                    IdeaSetting {
                        id: settingDelegate
                        required property var modelData
                        setting: modelData
                        objectName: setting.p_name
                        
                        anchors.centerIn: setting.p_name == "frequency" ? parent : undefined // TODO: is "frequency" the center?

                        Component.onCompleted: {
                            settingRepeater.objectArray.push(settingDelegate)
                            
                            // Check if all items are populated
                            if (settingRepeater.objectArray.length === settingRepeater.count) {
                                console.log("All delegates are ready:")
                                for (let i = 0; i < settingRepeater.objectArray.length; i++) {
                                    let child = settingRepeater.objectArray[i]
                                    
                                    if(child.setting.p_under != "")
                                    {
                                        console.log(child.objectName + " under " + child.setting.p_under)
                                        let foundItem = settingRepeater.objectArray.find(obj => obj.objectName === child.setting.p_under);
                                        if (foundItem) {
                                            child.under = foundItem;
                                        } else {
                                            console.log("Object not found");
                                        }
                                    }
                                    if(child.setting.p_rightOf != "")
                                    {
                                        console.log(child.objectName + " right of " + child.setting.p_rightOf)
                                        let foundItem = settingRepeater.objectArray.find(obj => obj.objectName === child.setting.p_rightOf);
                                        if (foundItem) {
                                            child.rightOf = foundItem;
                                        } else {
                                            console.log("Object not found");
                                        }
                                    }
                                    if(child.setting.p_leftOf != "")
                                    {
                                        console.log(child.objectName + " left of " + child.setting.p_leftOf)
                                        let foundItem = settingRepeater.objectArray.find(obj => obj.objectName === child.setting.p_leftOf);
                                        if (foundItem) {
                                            child.leftOf = foundItem;
                                        } else {
                                            console.log("Object not found");
                                        }
                                    }
                                    if(child.setting.p_over != "")
                                    {
                                        console.log(child.objectName + " over " + child.setting.p_over)
                                        let foundItem = settingRepeater.objectArray.find(obj => obj.objectName === child.setting.p_over);
                                        if (foundItem) {
                                            child.over = foundItem;
                                        } else {
                                            console.log("Object not found");
                                        }
                                    }
                                }
                            }
                        }
                    }
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
