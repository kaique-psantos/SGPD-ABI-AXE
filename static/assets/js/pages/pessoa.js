function mascaraCPF(campo) {
    var cpf = campo.value.replace(/\D/g, ''); // Remove qualquer caractere não numérico
    if (cpf.length <= 3) {
        campo.value = cpf;
    } else if (cpf.length <= 6) {
        campo.value = cpf.replace(/(\d{3})(\d{1,})/, '$1.$2');
    } else if (cpf.length <= 9) {
        campo.value = cpf.replace(/(\d{3})(\d{3})(\d{1,})/, '$1.$2.$3');
    } else {
        campo.value = cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{1,})/, '$1.$2.$3-$4');
    }
}

function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');

    if (cpf.length !== 11) {
        return false;
    }

    if (/^(\d)\1{10}$/.test(cpf)) {
        return false;
    }

    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let primeiroDigito = (soma * 10) % 11;
    if (primeiroDigito === 10 || primeiroDigito === 11) {
        primeiroDigito = 0;
    }
    if (parseInt(cpf.charAt(9)) !== primeiroDigito) {
        return false;
    }

    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    let segundoDigito = (soma * 10) % 11;
    if (segundoDigito === 10 || segundoDigito === 11) {
        segundoDigito = 0;
    }
    if (parseInt(cpf.charAt(10)) !== segundoDigito) {
        return false;
    }

    return true;
}

// Função para verificar se o CPF já está cadastrado
async function verificarDuplicidadeCPF(cpf) {
    const pessoa_id = document.getElementById('pessoa_id')?.value || '';
    const url = `{% url 'verificar_cpf' %}?cpf=${cpf}&pes_cod=${pessoa_id}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        return data.existe;
    } catch (error) {
        console.error('Erro ao verificar duplicidade de CPF:', error);
        return false; // Caso ocorra erro, assume que o CPF não está duplicado
    }
}

// Função para validar o formulário
async function validarFormulario(event) {
    event.preventDefault(); // Impede o envio automático do formulário

    const cpf = document.getElementById('InputCPF').value;

    // Verifica se o CPF é válido
    if (!validarCPF(cpf)) {
        alert('CPF inválido. Por favor, insira um CPF válido.');
        return; // Impede o envio do formulário
    }

    // Verifica se o CPF já está cadastrado
    const existe = await verificarDuplicidadeCPF(cpf);

    if (existe) {
        alert('Este CPF já está cadastrado. Por favor, insira um CPF diferente.');
        return; // Impede o envio do formulário
    }

    // Se o CPF for válido e não duplicado, exibe a mensagem de sucesso e envia o formulário
    // alert('Salvo com sucesso!');
    document.forms[0].submit();
}
//mascara Celular e Telefone
function mascaraCelular(campo) {
    var celular = campo.value.replace(/\D/g, ''); 
    if (celular.length <= 2) {
        campo.value = celular; 
    } else if (celular.length <= 7) {
        campo.value = celular.replace(/^(\d{2})(\d{1,})/, '($1) $2'); 
    } else {
        campo.value = celular.replace(/^(\d{2})(\d{5})(\d{1,})/, '($1) $2-$3'); 
    }
}

function mascaraTelefone(campo) {
    var telefone = campo.value.replace(/\D/g, ''); 
    if (telefone.length <= 2) {
        campo.value = telefone; 
    } else if (telefone.length <= 6) {
        campo.value = telefone.replace(/^(\d{2})(\d{1,})/, '($1) $2'); 
    } else {
        campo.value = telefone.replace(/^(\d{2})(\d{4})(\d{1,})/, '($1) $2-$3'); 
    }
}

function validarDatas() {
    var dataCadastro = document.getElementById("InputDataCadastro").value;
    var dataSaida = document.getElementById("InputDataSaida").value;

    if (dataCadastro && dataSaida) {
        if (dataSaida < dataCadastro) {
            alert("A data de saída não pode ser menor que a data de cadastro.");
            document.getElementById("InputDataSaida").value = ""; // Limpa a Data de Saída
        } else if (dataCadastro > dataSaida) {
            alert("A data de cadastro não pode ser maior que a data de saída.");
            document.getElementById("InputDataCadastro").value = ""; // Limpa a Data de Cadastro
        }
    }
}
document.addEventListener("DOMContentLoaded", function() {
    // Definir estado inicial do formulário
    toggleDataSaida();
});

function toggleDataSaida() {
    var checkbox = document.getElementById('exampleCheckbox');
    var dataSaida = document.getElementById('InputDataSaida');
    var dataSaidaLabel = document.getElementById('dataSaidaLabel');
    
    if (checkbox.checked) {
        dataSaida.disabled = true;
        dataSaida.removeAttribute('required');
        removeAsterisk(dataSaidaLabel);
    } else {
        dataSaida.disabled = false;
        dataSaida.setAttribute('required', 'required');
        addAsterisk(dataSaidaLabel);
    }
}

function addAsterisk(label) {
    var asterisk = document.createElement('span');
    asterisk.className = 'required-asterisk';
    asterisk.innerText = '*';
    if (!label.querySelector('.required-asterisk')) {
        label.appendChild(asterisk);
    }
}

function removeAsterisk(label) {
    var asterisk = label.querySelector('.required-asterisk');
    if (asterisk) {
        label.removeChild(asterisk);
    }
}
document.querySelector('.custom-file-input').addEventListener('change', function (e) {
    var fileName = document.getElementById("profilePicture").files[0].name;
    var nextSibling = e.target.nextElementSibling
    nextSibling.innerText = fileName
})


function previewImage(event) {
    const preview = document.getElementById('profilePicturePreview');
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        preview.src = '';
        preview.style.display = 'none';
    }
}


document.getElementById('myForm').addEventListener('submit', function(event) {
    // Check the validity of the form
    if (!this.checkValidity()) {
        // Prevent the form from submitting if it is invalid
        event.preventDefault();
        alert('Por favor, preencha todos os campos obrigatórios.');
    }
});