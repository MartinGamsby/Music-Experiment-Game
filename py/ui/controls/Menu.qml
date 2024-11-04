import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

ColumnLayout {
    id: menuRoot
    readonly property color backgroundColor: "#222222"
    
    component MusicButton: Button {        
        enabled: model ? model.p_music_state_id != MusicStateEnum.GENERATING : false // TODO: Not enough ...
        onClicked: {
            backend.ok_pressed(text)
        }
    }
	
    
    MusicButton {
        text: ""
    }
    MusicButton {
        text: "assets/town.mid"
    }
    MusicButton {
        text: "assets/onestop.mid"
    }
    MusicButton {
        text: "assets/flourish.mid"
    }
    MusicButton {
        text: "assets/AMEDLEY.MID"
    }
    MusicButton {
        text: "assets/cssamp1.mid"
    }
    MusicButton {
        text: "assets/test.mid"
    }
    MusicButton {
        text: "assets/ALMAR11-2016_09-10-04.mid"
    }
    CheckBox {
        id: cbGenerate
        text: "Generate Beautiful Midi files\n(Slower, might lag)"
        checked: model ? model.p_generate_mp3 : false
        onClicked: {
            model.set_generate_mp3(checked)
        }
    }
    Item {
        Layout.fillHeight: true
    }
    Image {
        id: image
        Layout.maximumWidth: 100
        Layout.maximumHeight: 100
         Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        source: "qrc:/logo"
        fillMode: Image.PreserveAspectFit
    }
}
