import Qt 4.7

    Item {
        property int itwidth 

        id: page 
        width: parent.width
        height: 40 

        MouseArea {
            anchors.fill: parent
            onClicked: { page.focus = true; }
            //onClicked: { page.focus = true; myText.openSoftwareInputPanel(); }
        }

        Text {
            text: name; x: 15; y: 8; height: 40; width: 370
            font.pixelSize: 18; font.bold: true; color: "white"
            style: Text.Outline; styleColor: "black"
            rotation: -8
        }

    }




