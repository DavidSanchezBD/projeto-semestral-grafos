# Script PowerShell para validação COM no Microsoft PowerPoint e exportação visual dos slides (Revisão v1)
$ErrorActionPreference = "Stop"

$Raiz = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$CaminhoPptx = Join-Path $Raiz "Entrega\Apresentacao_Caso_Fake_News.pptx"
$PastaExport = Join-Path $PSScriptRoot "slides_exportados"

if (-not (Test-Path $CaminhoPptx)) {
    throw "Arquivo PPTX não encontrado em: $CaminhoPptx"
}

if (-not (Test-Path $PastaExport)) {
    New-Item -ItemType Directory -Path $PastaExport | Out-Null
}

Write-Host "Abrindo PowerPoint via COM para aplicar/validar transições e exportar lâminas..."
$ppt = New-Object -ComObject PowerPoint.Application
try {
    # msoFalse = 0 para WithWindow (modo silencioso)
    $pres = $ppt.Presentations.Open($CaminhoPptx, 0, 0, 0)

    # Configura transição suave (ppEffectFade = 1793 / ppTransitionSpeedMedium = 2) e exporta PNG 1920x1080
    $idx = 1
    foreach ($slide in $pres.Slides) {
        $slide.SlideShowTransition.EntryEffect = 1793 # ppEffectFade
        $slide.SlideShowTransition.Duration = 0.6
        $slide.SlideShowTransition.AdvanceOnClick = -1 # msoTrue

        $arqPng = Join-Path $PastaExport ("slide_{0:D2}.png" -f $idx)
        $slide.Export($arqPng, "PNG", 1920, 1080)
        Write-Host ("Exportado Slide {0}: {1}" -f $idx, $arqPng)
        $idx++
    }

    $pres.Save()
    $pres.Close()
    Write-Host "Apresentação validada e imagens exportadas com sucesso!"
}
finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
