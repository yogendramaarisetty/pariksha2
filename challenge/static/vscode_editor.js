require(['vs/editor/editor.main'], function () {

        monaco.editor.defineTheme('myCustomTheme', {
            base: 'vs-dark', // can also be vs-dark or hc-black
            inherit: true, // can also be false to completely replace the builtin rules
            rules: [
                { background: '#1c2434' },
                { token: '', foreground: 'D2D2D2', background: '1C2430' },
                { token: 'invalid', foreground: 'f44747' },
                { token: 'emphasis', fontStyle: 'italic' },
                { token: 'strong', fontStyle: 'bold' },
                { token: 'variable', foreground: '74B0DF' },
                { token: 'variable.predefined', foreground: '4864AA' },
                { token: 'variable.parameter', foreground: '9CDCFE' },
                { token: 'constant', foreground: '569CD6' },
                { token: 'comment', foreground: '608B4E' },
                { token: 'number', foreground: 'B5CEA8' },
                { token: 'number.hex', foreground: '5BB498' },
                { token: 'regexp', foreground: 'B46695' },
                { token: 'annotation', foreground: 'cc6666' },
                { token: 'type', foreground: 'f78c6c' },
                { token: 'delimiter', foreground: '89ddff' },
                { token: 'delimiter.html', foreground: '808080' },
                { token: 'delimiter.xml', foreground: '808080' },
                { token: 'tag', foreground: '569CD6' },
                { token: 'tag.id.pug', foreground: '4F76AC' },
                { token: 'tag.class.pug', foreground: '4F76AC' },
                { token: 'meta.scss', foreground: 'A79873' },
                { token: 'meta.tag', foreground: 'CE9178' },
                { token: 'metatag', foreground: 'DD6A6F' },
                { token: 'metatag.content.html', foreground: '9CDCFE' },
                { token: 'metatag.html', foreground: '569CD6' },
                { token: 'metatag.xml', foreground: '569CD6' },
                { token: 'metatag.php', fontStyle: 'bold' },
                { token: 'key', foreground: '9CDCFE' },
                { token: 'string.key.json', foreground: '9CDCFE' },
                { token: 'string.value.json', foreground: 'CE9178' },
                { token: 'attribute.name', foreground: '9CDCFE' },
                { token: 'attribute.value', foreground: 'CE9178' },
                { token: 'attribute.value.number.css', foreground: 'B5CEA8' },
                { token: 'attribute.value.unit.css', foreground: 'B5CEA8' },
                { token: 'attribute.value.hex.css', foreground: '82aaff' },
                { token: 'string', foreground: 'c3e88d' },
                { token: 'string.sql', foreground: 'FF0000' },
                { token: 'keyword', foreground: 'c792ea', fontStyle: 'bold' },
                { token: 'keyword.flow', foreground: 'C586C0' },
                { token: 'keyword.json', foreground: 'CE9178' },
                { token: 'keyword.flow.scss', foreground: '569CD6' },
                { token: 'operator.scss', foreground: '909090' },
                { token: 'operator.sql', foreground: '778899' },
                { token: 'operator.swift', foreground: '909090' },
                { token: 'predefined.sql', foreground: 'FF00FF' },
            ],
            colors: {
                'editor.foreground': '#ababab',
                'editor.background': '#1c2434'
            }
            
        });
       

       editor = monaco.editor.create(document.getElementById('editor'), {
            value: [
                'function x() {',
                '\tconsole.log("Hello world!");',
                '}',
                
            ].join('\n'),
            language: 'javascript',
            theme: "myCustomTheme",
            automaticLayout: true,
            readOnly: false,
                mouseWheelZoom: true,
                // glyphMargin:true,
            fontSize: '17px'
        });

        // editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_C, () => null);
        // editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_V, () => null);
        // // editor.onDidChangeCursorSelection(
        //   () => {
        //     const { column, lineNumber } = this.editor.getPosition();
        //     editor.setPosition({ lineNumber, column });
        //   },
        // );

var currentActiveQuestion = null;
var currentActiveLanguage = $("#language option:first").val();
var editor = monaco.editor.getModels()[0];
$hideContainer = $('#q_hider');
$questionPage = $('#question_view');
    
    $('.q_btn').on('click',function(){
        console.log(this);
        $questionPage.children().appendTo($hideContainer);
        if(currentActiveQuestion!=null) {
            $(`#${currentActiveQuestion}`).removeClass('active');
        }
        get_codes(this.id);
        $(`#${this.id}`).addClass('active');
        $(`#desc_${this.id}`).appendTo($questionPage);
    })
    function get_codes(q_id){
        currentActiveQuestion = q_id;
        console.log(currentActiveQuestion);
        $.ajax({
            type: 'GET',url: '',dataType: 'json',cache: false,async: true,
            data: {
               csrfmiddlewaretoken: csrf_token,
               qid: q_id
            },
            success: function(json){
                console.log(json);
            },
            error: function(err){
                console.log(err);
            }
     });

    }
    $("#language").on("change",function(){
        currentActiveLanguage = this.value;
        changeLanguage(this.value);
    });

    function changeLanguage(lang){
        monaco.editor.setModelLanguage(editor,lang);
    }

    var btnLoaderElement = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Running...`;

    $('#run').on('click',function(){
        $('#run').prop('disabled',true);
        $('#run').html(btnLoaderElement);
        console.log(currentActiveQuestion)
        $.ajax({
            type: 'POST',url: '',dataType: 'json',cache: false,async: true,
            data: {
               csrfmiddlewaretoken: csrf_token,
               qid: currentActiveQuestion,
               language: currentActiveLanguage,
               code: editor.getValue()
            },
            success: function(json){
                alert(json);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
             }
     });
     $('#run').prop('disabled',false);
     $('#run').html('Run');
    });
      
    });


