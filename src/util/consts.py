uiConsts = {
    "ApplicationMinWidth": 800,
    "ApplicationMinHeight": 600,
    "ToolbarPadding": 8,
    "ToolbarTitleFontSize": 18,
    "ArtLayoutMargins": 32,
    "DrawerWidthCoefficient": 0.25,
    "ImageDialogWidthCoefficient": 0.85,
    "ImageDialogImageWidthCoefficient": 0.65,
    "DialogItemSpacingVert": 16,
    "DialogItemSpacingHoriz": 24,
    "DialogHelpImageSize": 16,
    "TooltipDelay": 100,
    "ArtListItemHeight": 180,
    "ArtListItemElevation": 3,
    "ArtListItemFontSize": 16,
    "ArtListItemImageHeight": 135,
    "ArtListItemMargin": 18,
    "ArtListItemAnimationDuration": 150,
    "AddImageDialogPathBoxLeftMargin": 2,
    "AddImageDialogPathBoxRightMargin": 8,
    "DefaultArtSize": 10,
    "DefaultAnimationDuration": 1.0,

    "ProjectName": "ASCII Art",
    "AuthorName": "Ivan Menshikov",
    "ProjectDomain": "https://gitlab.fit.cvut.cz/BI-PYT/b201/menshiva/tree/ascii-art",
    "DrawerTitle": "Image list",
    "PlayButtonText": "Play animation",
    "StopButtonText": "Stop animation",
    "SettingsText": "Settings",
    "AddImgButtonText": "Add image",
    "AddImgEffectsText": "Image effects",
    "AddImgContrastEffectText": "Contrast",
    "AddImgNegativeEffectText": "Negative",
    "AddImgConvolutionEffectText": "Convolution",
    "AddImgEmbossEffectText": "Emboss",
    "ArtListItemPropertiesBtn": "Properties",
    "ArtListItemSaveTxtBtn": "Export to text file",
    "ArtListItemRemoveBtn": "Remove image",
    "AddImageDialogNameTitle": "Art name",
    "AddImageDialogImgPathTitle": "Path to image...",
    "AddImageDialogBrowseBtn": "Browse",
    "AddImageDialogAddBtn": "Add",
    "AddImageDialogSaveBtn": "Save",
    "ApplyText": "Apply",
    "CancelText": "Cancel",
    "SettingsThemeTitle": "Theme",
    "SettingsThemeModels": ["Light", "Dark"],
    "SettingsGSLevelTitle": "Grayscale level",
    "SettingsGSLevelTooltip": "Enter the sequence of symbols from darkest to lightest. "
                              "Your ASCII art will be shown by these symbols. "
                              "(Leave the field empty to use the default grayscale level)",
    "AddImageDialogRequiredTootlip": "Required field",
    "SliderTooltip": "Art size",
    "AnimationDuration": "Animation duration",
    "SupportedImageFormats": "*.pgm *.ppm *.jpg *.jpeg *.png",

    "DrawerButtonImgSrc": "../../drawable/menu.svg",
    "PlayButtonImgSrc": "../../drawable/play.svg",
    "StopButtonImgSrc": "../../drawable/pause.svg",
    "MoreButtonImgSrc": "../../drawable/more.svg",
    "AddImgButtonImgSrc": "../../drawable/add_image.svg",
    "SettingsIconHelpSrc": "../../drawable/help.svg",
    "AddImageIconRequiredSrc": "../../drawable/warning.svg",
    "ArtListInfoImgSrc": "../../drawable/more.svg",
    "FontSrc": "../font/modenine.ttf",

    "DefaultGrayscaleLevel": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'.",

    "ShadowColor": "#80212121",
    "SliderColor": "#00675b"
}

imageConsts = {
    "EmbossKernel": [
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
    ],
    "ConvolutionKernel": [
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ],
    "LuminanceCoefficients": [0.2126, 0.7152, 0.0722]
}
