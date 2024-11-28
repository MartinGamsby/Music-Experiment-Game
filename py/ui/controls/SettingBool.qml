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
    
    implicitWidth: cb.implicitWidth
    implicitHeight: cb.implicitHeight
    
    visible: setting ? setting.p_unlocked : false
        
    CenteredCheckBox {    
        id: cb
            
        text: setting ? tr(setting.p_name) : ""
        checked: setting ? setting.b : false
        onClicked: {
            setting.b = checked
        }
    }
    Tooltip {
        property string tr_name: setting ? (setting.p_name+"_desc") : "" 
        text: tr(tr_name)
        visible: (tr_name != text) ? ( cb.hovered || cb.visualFocus ) : false
    }
}