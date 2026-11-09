$ErrorActionPreference = "Stop"

$pptxPath = (Resolve-Path "Entrega\Apresentacao_Caso_Fake_News.pptx").Path
$pastaPng = (Resolve-Path "documentos\apresentacao").Path + "\slides_png"

$pptApp = New-Object -ComObject PowerPoint.Application
try {
    $pres = $pptApp.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)

    # 1. Configurar Transições de Slide (Suave / Fade)
    # ppEffectFadeSmoothly = 3844, ppEffectPushUp = 1537, ppEffectWipeLeft = 769
    for ($i = 1; $i -le $pres.Slides.Count; $i++) {
        $slide = $pres.Slides.Item($i)
        $tr = $slide.SlideShowTransition
        $tr.EntryEffect = 3844 # Fade suave
        $tr.Duration = 0.6     # 0.6 segundos
        $tr.AdvanceOnTime = [Microsoft.Office.Core.MsoTriState]::msoFalse
        $tr.AdvanceOnClick = [Microsoft.Office.Core.MsoTriState]::msoTrue
    }

    # 2. Configurar Animações de Entrada nas Formas (MainSequence)
    # Efeitos: msoAnimEffectFade = 10, msoAnimEffectZoom = 24, msoAnimEffectAppear = 1, msoAnimEffectFly = 2
    # Triggers: msoAnimTriggerOnPageClick = 1, msoAnimTriggerWithPrevious = 2, msoAnimTriggerAfterPrevious = 3

    # Slide 1: Carimbo CONFIDENCIAL e Imagem BFS
    $s1 = $pres.Slides.Item(1)
    foreach ($shape in $s1.Shapes) {
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "CONFIDENCIAL") {
            $eff = $s1.TimeLine.MainSequence.AddEffect($shape, 24, 0, 3) # Zoom
            $eff.Timing.Duration = 0.5
        }
        if ($shape.Type -eq 13) { # Imagem BFS
            $eff = $s1.TimeLine.MainSequence.AddEffect($shape, 10, 0, 3) # Fade suave
            $eff.Timing.Duration = 0.6
        }
    }

    # Slide 2: Balão + Carimbo FAKE NEWS + As 3 Perguntas
    $s2 = $pres.Slides.Item(2)
    foreach ($shape in $s2.Shapes) {
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "FAKE NEWS") {
            $eff = $s2.TimeLine.MainSequence.AddEffect($shape, 24, 0, 3) # Zoom impactante
            $eff.Timing.Duration = 0.4
        }
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "AS 3 PERGUNTAS") {
            $eff = $s2.TimeLine.MainSequence.AddEffect($shape, 10, 0, 1) # Fade no clique
            $eff.Timing.Duration = 0.5
        }
    }

    # Slide 3: Os 4 pilares aparecem em sequência elegante
    $s3 = $pres.Slides.Item(3)
    foreach ($shape in $s3.Shapes) {
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "VÉRTICES|ARESTAS|REPRESENTAÇÃO|OBJETIVOS GÊMEOS") {
            $eff = $s3.TimeLine.MainSequence.AddEffect($shape, 10, 0, 3) # Fade sequencial
            $eff.Timing.Duration = 0.3
        }
    }

    # Slide 4: Screenshot do software + Carimbo de custo
    $s4 = $pres.Slides.Item(4)
    foreach ($shape in $s4.Shapes) {
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "CUSTO: O\(V \+ E\)") {
            $eff = $s4.TimeLine.MainSequence.AddEffect($shape, 24, 0, 3) # Zoom
            $eff.Timing.Duration = 0.4
        }
        if ($shape.Type -eq 13) { # Imagem screenshot
            $eff = $s4.TimeLine.MainSequence.AddEffect($shape, 10, 0, 1) # Fade no clique
            $eff.Timing.Duration = 0.6
        }
    }

    # Slide 5: Carimbo PONTES VENCEM GRAU e Paradigma
    $s5 = $pres.Slides.Item(5)
    foreach ($shape in $s5.Shapes) {
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "AULA T23") {
            $eff = $s5.TimeLine.MainSequence.AddEffect($shape, 24, 0, 3) # Zoom
            $eff.Timing.Duration = 0.4
        }
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "PONTES VENCEM GRAU") {
            $eff = $s5.TimeLine.MainSequence.AddEffect($shape, 24, 0, 1) # Zoom no clique de ápice
            $eff.Timing.Duration = 0.5
        }
    }

    # Slide 6: Box da Demonstração e Carimbo Caso Encerrado
    $s6 = $pres.Slides.Item(6)
    foreach ($shape in $s6.Shapes) {
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "CASO ENCERRADO") {
            $eff = $s6.TimeLine.MainSequence.AddEffect($shape, 24, 0, 3) # Zoom
            $eff.Timing.Duration = 0.5
        }
        if ($shape.HasTextFrame -and $shape.TextFrame.TextRange.Text -match "DEMONSTRAÇÃO EM JAVA") {
            $eff = $s6.TimeLine.MainSequence.AddEffect($shape, 10, 0, 1) # Fade no clique
            $eff.Timing.Duration = 0.5
        }
    }

    $pres.Save()
    # Exporta os slides para PNG/JPG para inspeção
    $pres.SaveAs($pastaPng, 17) # ppSaveAsJPG = 17
    $pres.Close()
    Write-Host "Transições, animações e exportação concluídas com sucesso!"
} finally {
    $pptApp.Quit()
}
