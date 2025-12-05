Sub Autophoto()
MsgBox "The file name and searchable text should be the exact same, It is suggested use numeric for better results." & vbLf _
& "For the text - either Capital or Lower or Capital Lower, the format should be the same "
On Error Resume Next
ActiveDocument.Unit = cdrCentimeter
Dim MDfolder As String
Dim pg As Page
Dim p As Integer
Dim ShapeN As Shape
Dim Ashape As Integer
Ashape = InputBox("No. of shape where photo will be powerclipped ?" & vbNewLine & vbNewLine & "To Know Shape No. - View instruction in video My G Trick")
Set ShapeN = ActivePage.ActiveLayer.Shapes(Ashape)
If ShapeN.Selected = False Then ShapeN.CreateSelection
Dim x As Double, y As Double, w As Double, h As Double
Dim sra As ShapeRange, strTemp As String
Set sra = ActiveSelectionRange
If sra.count = 0 Then Exit Sub
ActiveDocument.ReferencePoint = cdrTopLeft
sra.GetPosition x, y
sra.GetSize w, h
x = Round(x, 3) & vbCrLf
y = Round(y, 3) & vbCrLf
w = Round(w, 3) & vbCrLf
MsgBox "The selected object is shape no. " & Ashape & " and width is " & w & vbNewLine & "where photo will be powerclipped"
p = ActiveDocument.Pages.count
MDfolder = CorelScriptTools.GetFolder & "\"
For u = 1 To 3
    With CreateObject("wscript.shell")
    .currentdirectory = MDfolder
    .Run "%comspec% /c ren *.png *.jpeg", 0, True
    .Run "%comspec% /c ren *.PNG *.jpeg", 0, True
    .Run "%comspec% /c ren *.jpg *.jpeg", 0, True
    .Run "%comspec% /c ren *.JPG *.jpeg", 0, True
    .Run "%comspec% /c ren *.JPE *.jpeg", 0, True
    .Run "%comspec% /c ren *.jpe *.jpeg", 0, True
    End With
Next u
    Dim FolderPath As String
    Dim path As String
    Dim count As Integer
    Dim FileName As String
    Dim o As Integer
    FolderPath = MDfolder
    path = FolderPath & "*.jpeg"
    FileName = Dir(path)
    Do While FileName <> ""
       count = count + 1
        FileName = Dir()
    Loop
    o = count
    Set Doc = ActiveDocument
    bFirst = True
    strFile = Dir(MDfolder & "*.jpeg")
    Dim i As Integer
    i = 0
    Dim barArray() As String
    ReDim Preserve barArray(o)
    Dim txt As TextRange
    Dim phFile As String
    While strFile <> ""
        barArray(i) = strFile
        strFile = Dir()
        i = i + 1
    Wend
ActiveDocument.ReferencePoint = cdrCenter
Dim s As Shape, n As Long, sr As ShapeRange
Dim j As String
For r = 0 To i
For Each pg In ActiveDocument.Pages
    pg.Activate
    Set sr = ActivePage.Shapes.FindShapes(, cdrTextShape)
    For Each s In sr
    j = s.Text.Story.Characters.All & ".jpeg"
        If barArray(r) = j Then
            pg.ActiveLayer.Import MDfolder & barArray(r)
            If pg.ActiveLayer.Ashape.Selected Then
                pg.ActiveLayer.Shapes(1).SetBoundingBox x, y, w, False
                pg.ActiveLayer.Shapes(1).AddToPowerClip pg.ActiveLayer.Shapes(Ashape + 1), cdrTrue
                If barArray(r) = j Then Exit For
            End If
        End If
    Next s
Next pg
Next r
    If p <> o Then
        MsgBox "Nos. of Photograph and No. of Pages was not SAME, Maybe few of photographs were left please check"
    End If
MsgBox "                        Done!" & vbLf _
& "This Code is provided by Rupinder Singh"
End Sub