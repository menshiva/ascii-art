import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15
import QtGraphicalEffects 1.15

Dialog {
    width: parent.width * Consts.DialogWidthCoefficient
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2
    title: Consts.SettingsButtonText
    modal: true
    closePolicy: Popup.NoAutoClose
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    ColumnLayout {
        anchors.fill: parent
        spacing: Consts.DialogItemSpacingHoriz

        GroupBox {
            Layout.fillWidth: true
            title: Consts.SettingsThemeTitle

            ComboBox {
                id: themeBox
                width: parent.width
                flat: true
                Material.foreground: parent.Material.foreground
                model: Consts.SettingsThemeModels
                currentIndex: settings.theme
            }
        }
        GroupBox {
            Layout.fillWidth: true

            label: RowLayout {
                Label {
                    Layout.leftMargin: 8
                    text: Consts.SettingsGSLevelTitle
                }
                Image {
                    source: Consts.SettingsIconHelpSrc
                    sourceSize.width: Consts.DialogHelpImageSize
                    sourceSize.height: Consts.DialogHelpImageSize
                    ToolTip.visible: ma.containsMouse
                    ToolTip.delay: Consts.TooltipDelay
                    ToolTip.text: Consts.SettingsGSLevelTooltip

                    MouseArea {
                        id: ma
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                    ColorOverlay {
                        anchors.fill: parent
                        source: parent
                        color: window.Material.foreground
                    }
                }
            }
            TextField {
                id: grayscaleBox
                width: parent.width
                text: settings.grayscale
                placeholderText: Consts.DefaultGrayscaleLevel
                selectByMouse: true
            }
        }
        GroupBox {
            Layout.fillWidth: true
            title: Consts.AnimationDuration

            Slider {
                id: durationBox
                width: parent.width
                snapMode: Slider.SnapAlways
                from: 0.1
                stepSize: 0.1
                to: 2.0
                value: settings.animationDuration.toFixed(1)

                ToolTip {
                    parent: durationBox.handle
                    visible: durationBox.pressed
                    text: durationBox.value.toFixed(1)
                }
            }
        }
    }
    footer: DialogButtonBox {
        Button {
            flat: true
            text: Consts.SettingsDialogSaveButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            onClicked: {
                settings.theme = themeBox.currentIndex
                settings.animationDuration = durationBox.value
                if (settings.grayscale != grayscaleBox.text) {
                    settings.grayscale = grayscaleBox.text
                    Gui.__apply_grayscale(settings.grayscale)
                }
            }
        }
        Button {
            flat: true
            text: Consts.DialogCancelButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            onClicked: {
                themeBox.currentIndex = settings.theme
                grayscaleBox.text = settings.grayscale
                durationBox.value = settings.animationDuration.toFixed(1)
            }
        }
    }
}