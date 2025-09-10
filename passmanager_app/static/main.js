function cancel(){
    pop = document.getElementById("message_pop"); 
    pop.remove()
}
setTimeout(() => {
    const pop = document.getElementById("message_pop"); 
    if (pop) pop.remove(); 
}, 2500); 
function togglePassword() {
    const passwordInput = document.getElementById("passwordField");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}
function link_open(){
    const links = document.getElementById("link").innerHTML; 
    window.open(links, "_blank")
}
function copy_text(){
     const pass_word = document.getElementById("passwordField").value; 
    navigator.clipboard.writeText(pass_word).then( ()=>{
        alert("PASSWORD COPIED ");
    })
}
function edit_section(){
    document.getElementById("edit_section").style.display ='flex';
}
function edit_sec_close(){
    document.getElementById("edit_section").style.display ='none';
}
function del_sel(){
    document.getElementById("delete_sec").style.display= 'flex'; 
}
function del_clos(){
     document.getElementById("delete_sec").style.display= 'none'; 
}

function dt_edt_sec(){
    document.getElementById("dt_edit_section").style.display = 'flex';
}

function dt_edt_sec_cls(){
    document.getElementById("dt_edit_section").style.display = 'none';
}
function dt_del_sec_but(){
    document.getElementById("dt_del_sec").style.display = 'flex';
}
function dt_del_sec_butcs(){
    document.getElementById("dt_del_sec").style.display = 'none';
}

function add_note_ft(){
    fields = document.getElementById("add_field"); 
    newField= document.createElement("div_add"); 
    newField.innerHTML = `
        <textarea name="field[]" placeholder="ADD CONTENT" required></textarea>
        <button type="button" onclick="removeField(this)" class="note_add_field-clc">✖</button>
    `; 
    fields.appendChild(newField);
}
function add_note_ft1() {
    const fields = document.getElementById("add_field");
    const newField = document.createElement("div1");
    newField.innerHTML = `
        <textarea name="field[]" placeholder="ADD CONTENT" required></textarea>
        <button type="button" onclick="removeField(this)" class="note_add_field-clc">✖</button>
    `;
    fields.appendChild(newField);
}

function removeField(button) {
    button.parentElement.remove();
}
function notes_dt_edt(){
    document.getElementById("notes_dt_div4").style.display = 'flex';
}
function notes_dt_edt_cls(){
     document.getElementById("notes_dt_div4").style.display = 'none';
}
function notes_dt_del(){
    document.getElementById("notes_dt_delsec").style.display = 'flex'; 
}
function notes_dt_delcnc(){
    document.getElementById("notes_dt_delsec").style.display = 'none'; 
}
function notes_dt_addnw(){
    document.getElementById("notesdt_add_nw").style.display = 'flex';
}
function notes_dt_addclc(){
    document.getElementById("notesdt_add_nw").style.display = 'none';
}


