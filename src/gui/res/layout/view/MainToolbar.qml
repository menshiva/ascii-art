import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ToolBar {
    Material.foreground: "white"
    leftPadding: Consts.ToolbarPadding
    rightPadding: leftPadding

    RowLayout {
        anchors.fill: parent

        ToolButton {
            icon.source: Consts.DrawerButtonImgSrc
            onClicked: drawer.open()
        }
        Label {
            Layout.fillWidth: true
            leftPadding: Consts.ToolbarTitlePadding
            text: Consts.ToolbarTitle
            font.pixelSize: Consts.ToolbarTitleFontSize
        }
        Slider {
            id: artSizeSlider
            objectName: "artSizeSlider"
            Material.accent: Consts.SliderColor
            snapMode: Slider.SnapAlways
            from: 3
            stepSize: 1
            to: 25
            value: Consts.DefaultArtSize
            onMoved: {
                artLayout.font.pixelSize = value
                Gui.__draw_art()
            }

            ToolTip {
                parent: artSizeSlider.handle
                visible: artSizeSlider.hovered && !artSizeSlider.pressed
                text: Consts.SliderTooltip
            }
            ToolTip {
                parent: artSizeSlider.handle
                visible: artSizeSlider.pressed
                text: artSizeSlider.value
            }
        }
        ToolSeparator {}
        ToolButton {
            objectName: "playAnimBtn"
            enabled: false
            icon.source: Consts.PlayButtonImgSrc
            text: Consts.PlayButtonText
            onClicked: Gui.__start_animation()
        }
        ToolButton {
            objectName: "stopAnimBtn"
            enabled: false
            icon.source: Consts.StopButtonImgSrc
            text: Consts.StopButtonText
            onClicked: Gui.__stop_animation()
        }
        ToolSeparator {}
        ToolButton {
            icon.source: Consts.MoreButtonImgSrc
            onClicked: settingsMenu.open()

            Menu {
                id: settingsMenu
                y: parent.height
                topPadding: 0
                bottomPadding: topPadding

                Action {
                    text: Consts.SettingsButtonText
                    onTriggered: {
                        Gui.__stop_animation()
                        settingsDialog.open()
                    }
                }
            }
        }
    }
}