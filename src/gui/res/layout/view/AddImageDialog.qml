import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15
import QtGraphicalEffects 1.15

Dialog {
    property int itemIndex: -1
    width: parent.width * Consts.AddImageDialogWidthCoefficient
    anchors.centerIn: Overlay.overlay
    title: Consts.AddImgButtonText
    modal: true
    closePolicy: Popup.NoAutoClose
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    RowLayout {
        anchors.fill: parent
        spacing: Consts.DialogItemSpacingHoriz

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: Consts.DialogItemSpacingVert

            GroupBox {
                Layout.fillWidth: true

                label: RowLayout {
                    Label {
                        Layout.leftMargin: 8
                        text: Consts.AddImageDialogNameTitle
                    }
                    Image {
                        source: Consts.AddImageIconRequiredSrc
                        sourceSize.width: Consts.DialogHelpImageSize
                        sourceSize.height: Consts.DialogHelpImageSize
                        ToolTip.visible: addMa1.containsMouse
                        ToolTip.delay: Consts.TooltipDelay
                        ToolTip.text: Consts.AddImageDialogRequiredTootlip

                        MouseArea {
                            id: addMa1
                            anchors.fill: parent
                            hoverEnabled: true
                        }
                        ColorOverlay {
                            anchors.fill: parent
                            source: parent
                            color: Material.foreground
                        }
                    }
                }
                TextField {
                    id: addImageDialogNameBox
                    width: parent.width
                    selectByMouse: true
                    onTextChanged: {
                        addImageBtn.enabled = addImageDialogNameBox.text != "" && addImageDialogPathBox.text != ""
                    }
                }
            }
            GroupBox {
                Layout.fillWidth: true

                label: RowLayout {
                    Label {
                        Layout.leftMargin: 8
                        text: Consts.AddImageDialogImgPathTitle
                    }
                    Image {
                        source: Consts.AddImageIconRequiredSrc
                        sourceSize.width: Consts.DialogHelpImageSize
                        sourceSize.height: Consts.DialogHelpImageSize
                        ToolTip.visible: addMa2.containsMouse
                        ToolTip.delay: Consts.TooltipDelay
                        ToolTip.text: Consts.AddImageDialogRequiredTootlip

                        MouseArea {
                            id: addMa2
                            anchors.fill: parent
                            hoverEnabled: true
                        }
                        ColorOverlay {
                            anchors.fill: parent
                            source: parent
                            color: Material.foreground
                        }
                    }
                }
                RowLayout {
                    anchors.fill: parent

                    TextField {
                        id: addImageDialogPathBox
                        objectName: "addImageDialogPathBox"
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.leftMargin: Consts.AddImageDialogPathBoxLeftMargin
                        Layout.rightMargin: Consts.AddImageDialogPathBoxRightMargin
                        readOnly: true
                        onTextChanged: {
                            addImageBtn.enabled = addImageDialogNameBox.text != "" && addImageDialogPathBox.text != ""
                        }
                    }
                    Button {
                        objectName: "addImageDialogBrowseBtn"
                        text: Consts.AddImageDialogBrowseBtn
                        highlighted: true
                        enabled: itemIndex == -1
                    }
                }
            }
        }
        GroupBox {
            title: Consts.AddImgEffectsText

            ColumnLayout {
                anchors.fill: parent

                CheckBox {
                    id: contrastEffect
                    text: Consts.AddImgContrastEffectText
                }
                CheckBox {
                    id: negativeEffect
                    text: Consts.AddImgNegativeEffectText
                }
                CheckBox {
                    id: convolutionEffect
                    text: Consts.AddImgConvolutionEffectText
                }
            }
        }
    }
    footer: DialogButtonBox {
        Button {
            id: addImageBtn
            enabled: false
            flat: true
            text: itemIndex == -1 ? Consts.AddImageDialogAddBtn : Consts.AddImageDialogSaveBtn
            DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
            onClicked: {
                if (itemIndex == -1) {
                    ArtModels.add_art(
                        addImageDialogNameBox.text,
                        addImageDialogPathBox.text,
                        contrastEffect.checked,
                        negativeEffect.checked,
                        convolutionEffect.checked
                    )
                    addImageDialogNameBox.text = ""
                    addImageDialogPathBox.text = ""
                }
                else {
                    ArtModels.edit_art(
                        itemIndex,
                        addImageDialogNameBox.text,
                        addImageDialogPathBox.text,
                        contrastEffect.checked,
                        negativeEffect.checked,
                        convolutionEffect.checked
                    )
                    addImageDialog.close()
                }
            }
        }
        Button {
            flat: true
            text: Consts.DialogCancelButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
        }
    }

    function openDialog(index, name, path, contrast, negative, convolution) {
        itemIndex = index
        addImageDialogNameBox.text = name
        addImageDialogPathBox.text = path
        contrastEffect.checked = contrast
        negativeEffect.checked = negative
        convolutionEffect.checked = convolution
        open()
    }
}