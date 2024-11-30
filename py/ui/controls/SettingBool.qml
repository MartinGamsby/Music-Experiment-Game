import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import QtQuick.Dialogs

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    required property Setting setting
    property bool alignCenter: false
    
    Layout.fillWidth: true
    Layout.fillHeight: false
    
    implicitWidth: alignCenter ? (Math.max(140, cb.implicitWidth)) : cb.implicitWidth
    implicitHeight: alignCenter ? (Math.max(90,cb.implicitHeight)) : cb.implicitHeight
    
    visible: setting ? setting.p_unlocked : false    
    
    function getName(name) {
        let tr_name = tr(name)
        if( tr_name == name ){
            //hack for instrument:
            name = name.replace("instrument_","")
            return name
                .replace(/_/g, ' ') // Replace underscores with spaces
                .split(' ')         // Split into words
                .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize each word
                .join(' ');         // Join the words back with spaces
                }
        return tr_name
    }
     
    // TODO: Loader or something        
    CheckBox {    
        id: cb
        visible: !alignCenter
        enabled: setting ? setting.p_enabled : false
            
        text: setting ? getName(setting.p_name) : ""
        checked: setting ? setting.b : false
        onClicked: {
            setting.b = checked
        }
    }
    CenteredCheckBox {    
        id: centeredCb
        visible: !cb.visible
        enabled: setting ? setting.p_enabled : false
        anchors.centerIn: parent
            
        text: cb.text
        checked: cb.checked
        onClicked: {
            setting.b = checked
        }
    }
    Tooltip {
        property string tr_name: setting ? (setting.p_name+".desc") : "" 
        text: tr(tr_name)
        visible: (tr_name != text) ? ( cb.hovered || cb.visualFocus || centeredCb.hovered || centeredCb.visualFocus ) : false
    }
}