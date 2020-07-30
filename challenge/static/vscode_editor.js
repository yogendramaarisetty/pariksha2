require(['vs/editor/editor.main'], function () {

        monaco.editor.defineTheme('myCustomTheme', {
            base: 'vs-dark', // can also be vs-dark or hc-black
            inherit: true, // can also be false to completely replace the builtin rules
            rules: [
                { background: '#1c2434' },
                { token: '', foreground: '61afef', background: '1C2430' },
                { token: 'invalid', foreground: 'f44747' },
                { token: 'emphasis', fontStyle: 'italic' },
                { token: 'strong', fontStyle: 'bold' },
                { token: 'variable', foreground: '74B0DF' },
                { token: 'variable.predefined', foreground: '4864AA' },
                { token: 'variable.parameter', foreground: '9CDCFE' },
                { token: 'constant', foreground: '569CD6' },
                { token: 'comment', foreground: '7f848e' },
                { token: 'number', foreground: 'B5CEA8' },
                { token: 'number.hex', foreground: '5BB498' },
                { token: 'regexp', foreground: 'B46695' },
                { token: 'annotation', foreground: 'cc6666' },
                { token: 'type', foreground: 'f78c6c' },
                { token: 'delimiter', foreground: 'dcdcdc' },
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
                { token: 'string', foreground: '98c379' },
                { token: 'string.sql', foreground: 'FF0000' },
                { token: 'keyword', foreground: 'e06c75', fontStyle: 'bold' },
                { token: 'keyword.flow', foreground: 'C586C0' },
                { token: 'keyword.json', foreground: 'CE9178' },
                { token: 'keyword.flow.scss', foreground: '569CD6' },
                { token: 'operator.scss', foreground: '909090' },
                { token: 'operator.sql', foreground: '778899' },
                { token: 'operator.swift', foreground: '909090' },
                { token: 'predefined.sql', foreground: 'FF00FF' },
            ],
            colors: {
                'editor.foreground': '#61afef',
                'editor.background': '#1c2434'
            }
            
        });
       

       var Ieditor = monaco.editor.create(document.getElementById('editor'), {
            value: '',
            language: 'javascript',
            theme: "myCustomTheme",
            automaticLayout: true,
            readOnly: false,
                mouseWheelZoom: true,
                glyphMargin:true,
            fontSize: '16px'
        });
        
// var decorations = editor.deltaDecorations([], [
// 	{
// 		range: new monaco.Range(3,1,3,1),
// 		options: {
// 			isWholeLine: true,
// 			className: 'myContentClass',
// 			glyphMarginClassName: 'myGlyphMarginClass'
// 		}
// 	}
// ]);

        // editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_C, () => null);
        // editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_V, () => null);
        // // editor.onDidChangeCursorSelection(
        //   () => {
        //     const { column, lineNumber } = this.editor.getPosition();
        //     editor.setPosition({ lineNumber, column });
        //   },
        // );

function showEditorLoad(){
    $('#editor').LoadingOverlay("show", {
        image       : "",
        fontawesome : "",                              // String/Boolean
        background: "#111827",
        custom : customElement,
        size                    : 50   ,                             // Float/String/Boolean
        minSize                 : 20    ,                            // Integer/String
        maxSize                 : 80    ,                           // Integer/String
        // Misc
        direction               : "column",                          // String
        fade                    : [400, 200],                        // Array/Boolean/Integer/String
        resizeInterval          : 50         ,                       // Integer
        zIndex                  : 2147483647                        // Integer

    });
}
function hideEditorLoad(){
    $('#editor').LoadingOverlay("hide");
}
function showConsoleLoad(){

 $('#console').LoadingOverlay("show", {
        image       : "",
        fontawesome : "",                              // String/Boolean
        background: "#111827",
        custom : roundLoader,
        size                    : 50   ,                             // Float/String/Boolean
        minSize                 : 20    ,                            // Integer/String
        maxSize                 : 120    ,                           // Integer/String
        // Misc
        text                    : "Running your code....."    ,                            // String/Boolean
textAnimation           : ""                   ,             // String/Boolean
textAutoResize          : true                  ,            // Boolean
textResizeFactor        : 0.3                  ,            // Float
textColor               : "#202020"              ,           // String/Boolean
textClass               : "loading-text"                    ,            // String/Boolean
textOrder               : 4,
        direction               : "column",                          // String
        fade                    : [400, 200],                        // Array/Boolean/Integer/String
        resizeInterval          : 50         ,                       // Integer
        zIndex                  : 2147483647                        // Integer

    });
}
function hideConsoleLoad(){
$('#console').LoadingOverlay("hide");
}
var currentActiveQuestion = null;
var currentQuestionCodes = null;
var currentActiveLanguage = $("#language option:first").val();
var editor = monaco.editor.getModels()[0];
var $consoleHider = $("#console_hider");
var $console = $("#console");
var $customInputBtn = $("#custom_input");
var $testcaseResultsBtn = $("#testcase_results"); 
var $run = $('#run');
var $hideContainer = $('#q_hider');
var $questionPage = $('#question_view');

    
    

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
        showEditorLoad();
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
                currentQuestionCodes = json;
                changeLanguage(currentActiveLanguage);
                hideEditorLoad();
              
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                console.log(errorThrown);
            }
     });

    }
   
    $("#language").on("change",function(){
        currentActiveLanguage = this.value;
        changeLanguage(this.value);
    });

    function changeLanguage(lang){
        monaco.editor.setModelLanguage(editor,lang);
        editor.setValue(currentQuestionCodes['codes'][lang]);
    }

    Ieditor.onDidChangeModelContent(e => {
        currentQuestionCodes['codes'][currentActiveLanguage] = editor.getValue(); //upadte current question code data
    });
    
    var btnLoaderElement = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Running...`;

    $run.on('click',function(){
     showConsoleLoad();
        $run.prop('disabled',true);
        $run.html(btnLoaderElement);
        $.ajax({
            type: 'POST',url: '',dataType: 'json',cache: false,async: true,
            data: {
               csrfmiddlewaretoken: csrf_token,
               qid: currentActiveQuestion,
               language: currentActiveLanguage,
               code: editor.getValue()
            },
            success: function(response){
            splitV.setSizes([10, 90]);
               console.log(JSON.stringify(response));
               createRunCard(response);
               $console.children().appendTo($consoleHider);
               $("#run-card").appendTo($console);
            },
            statusCode: {
                404: function() {
                  alert( "page not found" );
                },
                500: function(){
                    alert( "internal server error" );
                },

              },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
                hideConsoleLoad();
                $run.prop('disabled',false);
                $run.html('<i class="fas fa-play"></i> Run');
             }
     }).done(function() {
     hideConsoleLoad();
        $('#run').prop('disabled',false);
        $('#run').html('<i class="fas fa-play"></i> Run');
        $console.children().appendTo($consoleHider);
        $("[data=run]").appendTo($console);
      });

      function createRunCard(res){
            $("#run-card").html(function(){
                var html = "";
                for(var i=0;i<res.length;i++){
                    var customClass=res[i]["class"];
                    var wrap = "<div class=\"shadow-lg dtheme-c2 m-auto pt-2 pb-2 pr-3 pl-3\">";
                    var statusIcons = {
                    "SUCCESS" : `<i class="far fa-check-circle"></i>`,
                    "WRONG": `<i class="fas fa-times"></i>`,
                    "CE":`<i class="fas fa-bug"></i>`,
                    "RE":`<i class="fas fa-exclamation-circle"></i>`,
                    "TLE":`<i class="far fa-clock"></i>`
                    };
                    var badgeClass={
                    "SUCCESS" : `success`,
                    "WRONG": `danger`,
                    "CE":"danger",
                    "RE":`warning`,
                    "TLE":`warning`
                    }
                    var tc_name = `<h5><span class="badge badge-dark">Sample testcase ${i}</span></h5>`;
//                    var heading = `<h4 class=${customClass}>${res[i]["status"]["description"]} <span>${statusIcons[customClass]}</span></h4>`;
                    var statusClass = `badge text-c1 badge-pill badge-`+customClass;
                    var status = `<span class='badge  badge-pill badge-${badgeClass[customClass]}'><span class="mr-1">${statusIcons[customClass]}</span>${res[i]["status"]["description"]}</span><br><br>`;
                    var message="";
                    if(customClass =="SUCCESS" || customClass =="WRONG"){
                         message+= `<label class="label">Sample Input</label><pre class=${customClass}>${res[i]["input"]}</pre>`
                         if(res[i]["msg"])
                         message += `<label class="label">Your Output</label><pre class=${customClass}>${res[i]["msg"]}</pre>`;
                         else
                         message += `<label class="label">Your Output</label><pre class=${customClass}>Your code didn\'t print anything</pre>`;
                         message += `<label class="label">Expected Output</label><pre class=${customClass}>${res[i]["expected"]}</pre>`;
                    }
                    else
                         message = `<label class="label">Message</label><pre class=${customClass}>${res[i]["msg"]}</pre>`;
                     html += wrap+tc_name+status+message+"</div><br>";
                }
                return html;
            })
      }
    
       }) 
    
    $testcaseResultsBtn.on('click',function(){
        $console.children().appendTo($consoleHider);
        $("[data=testcase_results]").appendTo($console);
    })
    





  
    });
      


