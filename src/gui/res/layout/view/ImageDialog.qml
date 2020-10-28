import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15
import QtGraphicalEffects 1.15

Dialog {
    property int itemIndex: -1
    width: parent.width * Consts.ImageDialogWidthCoefficient
    height: parent.height
    x: (parent.width - width) / 2
    y: 0
    title: Consts.AddImgButtonText
    modal: true
    closePolicy: Popup.NoAutoClose
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    RowLayout {
        anchors.fill: parent
        spacing: Consts.DialogItemSpacingHoriz

        Image {
            id: previewImg
            Layout.preferredWidth: parent.parent.width * Consts.ImageDialogImageWidthCoefficient
            Layout.fillHeight: true
            fillMode: Image.PreserveAspectFit
            cache: false
        }
        ColumnLayout {
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
                        addImageBtn.enabled = addImageDialogNameBox.text != ""
                                           && addImageDialogPathBox.text != ""
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
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.leftMargin: Consts.AddImageDialogPathBoxLeftMargin
                        Layout.rightMargin: Consts.AddImageDialogPathBoxRightMargin
                        readOnly: true
                        onTextChanged: {
                            addImageBtn.enabled = addImageDialogNameBox.text != ""
                                               && addImageDialogPathBox.text != ""
                        }
                    }
                    Button {
                        id: browseImgBtn
                        text: Consts.AddImageDialogBrowseBtn
                        highlighted: true
                        onClicked: {
                            addImageDialogPathBox.text = Gui.__browse_files()
                            previewImage()
                        }
                    }
                }
            }
            GroupBox {
                Layout.fillWidth: true
                title: Consts.AddImgEffectsText

                ColumnLayout {
                    anchors.horizontalCenter: parent.horizontalCenter

                    CheckBox {
                        id: contrastEffect
                        text: Consts.AddImgContrastEffectText
                        onClicked: previewImage()
                    }
                    CheckBox {
                        id: negativeEffect
                        text: Consts.AddImgNegativeEffectText
                        onClicked: previewImage()
                    }
                    CheckBox {
                        id: convolutionEffect
                        text: Consts.AddImgConvolutionEffectText
                        onClicked: previewImage()
                    }
                    CheckBox {
                        id: embossEffect
                        text: Consts.AddImgEmbossEffectText
                        onClicked: previewImage()
                    }
                }
            }
            ProgressBar {
                id: imgLoadingBar
                Layout.fillWidth: true
                indeterminate: true
                visible: false
            }
        }
    }
    footer: DialogButtonBox {
        Button {
            id: addImageBtn
            enabled: false
            flat: true
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            onClicked: Gui.__add_edit_art(itemIndex, addImageDialogNameBox.text)
        }
        Button {
            id: cancelImageBtn
            flat: true
            text: Consts.CancelText
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
        }
    }

    function setImageLoading(isLoading) {
        addImageDialogNameBox.enabled = !isLoading
        browseImgBtn.enabled = !isLoading
        contrastEffect.enabled = !isLoading
        negativeEffect.enabled = !isLoading
        convolutionEffect.enabled = !isLoading
        embossEffect.enabled = !isLoading
        addImageBtn.enabled = !isLoading
                              && addImageDialogNameBox.text != ""
                              && addImageDialogPathBox.text != ""
        cancelImageBtn.enabled = !isLoading
        imgLoadingBar.visible = isLoading
    }

    function setPreview(previewPath) {
        previewImg.source = ""
        previewImg.source = previewPath
    }

    function previewImage() {
        if (addImageDialogPathBox.text == "") return
        Gui.__preview_art(
            addImageDialogNameBox.text,
            addImageDialogPathBox.text,
            contrastEffect.checked,
            negativeEffect.checked,
            convolutionEffect.checked,
            embossEffect.checked,
            settings.grayscale
        )
    }

    function openDialog(index, preview, name, path, contrast, negative, convolution, emboss) {
        itemIndex = index
        setPreview(preview)
        browseImgBtn.enabled = itemIndex == -1
        addImageDialogNameBox.text = name
        addImageDialogPathBox.text = path
        contrastEffect.checked = contrast
        negativeEffect.checked = negative
        convolutionEffect.checked = convolution
        embossEffect.checked = emboss
        addImageBtn.text = itemIndex == -1 ? Consts.AddImageDialogAddBtn : Consts.AddImageDialogSaveBtn
        open()
    }
}