import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Button {
    font.pixelSize: 32
    required property string hl
    icon.color: "transparent"
    icon.width: 64
    icon.height: 32
    
    icon.source: "qrc:/flag_" + hl
    property bool isSelected: model ? (model.p_language.s.startsWith(hl)) : false
        
    implicitWidth: isSelected ? 240 : (hovered ? 240 : 96)
    
    onClicked: {
        backend.selectLanguage(hl)
    }
    Behavior on implicitWidth { 
        PropertyAnimation { easing.type: Easing.InOutQuad } 
    }
}
