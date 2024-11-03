import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Column {
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
}
