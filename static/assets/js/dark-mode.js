const themeSwitch = document.getElementById("theme-switch"); //our switch element
const themeIndicator = document.getElementById("theme-indicator"); //our theme icon
const page = document.body; //our document body

// To avoid any confusion, all variables are placed inside arrays.
// We will later use indexes to access these values.
const themeStates = ["light", "dark"]
const indicators = ["icon-moon", "icon-sun"]

// Now we check our local storage and get the value of our theme.
let currentTheme = localStorage.getItem("theme");

// This is a helper function to set the theme.
// We will pass in the index of our array.
function setTheme(theme) {
    localStorage.setItem("theme", themeStates[theme])
    updateChartColors(theme); // Atualiza as cores do gráfico com base no tema
}

// This is a helper function to set the icon.
// We will pass in the index of our array.
function setIndicator(theme) {
    // We remove all possible classes.
    themeIndicator.classList.remove(indicators[0])
    themeIndicator.classList.remove(indicators[1])
    // then we add our desired class name.
    themeIndicator.classList.add(indicators[theme])
}

// This is a helper function to set the page theme class.
// We will pass in the index of our array.
function setPage(theme) {
    // We will remove the existing classes,
    // and then we will add our current theme class.
    if (theme === 1){
        page.classList.add("dark")
    }else{
        page.classList.remove("dark")
    }
}

// Function to update the colors of the Plotly chart dynamically
function updateChartColors(theme) {
    const chartElements = document.querySelectorAll('.plotly-graph-div'); // Seleciona todos os gráficos Plotly

    chartElements.forEach(function(graphElement) {
        if (theme === 1) {  // Dark mode
            Plotly.relayout(graphElement, {
                'plot_bgcolor': '#2C394B',  // Fundo do gráfico
                'paper_bgcolor': '#2C394B', // Fundo ao redor do gráfico
                'font.color': 'white',      // Cor do texto
            });
        } else {  // Light mode
            Plotly.relayout(graphElement, {
                'plot_bgcolor': 'white',    // Fundo branco para tema claro
                'paper_bgcolor': 'white',   // Fundo branco
                'font.color': 'black',      // Cor do texto escuro
            });
        }
    });
}

// We'll check for the value and set our theme accordingly
if (currentTheme === null) {
    localStorage.setItem("theme", themeStates[0])
    setIndicator(0)
    setPage(0)
    themeSwitch.checked = true;
    updateChartColors(0); // Chama a função para atualizar o gráfico no carregamento inicial
}
if (currentTheme === themeStates[0]) {
    setIndicator(0)
    setPage(0)
    themeSwitch.checked = true;
    updateChartColors(0); // Chama a função para atualizar o gráfico no tema claro
}
if (currentTheme === themeStates[1]) {
    setIndicator(1)
    setPage(1)
    themeSwitch.checked = false;
    updateChartColors(1); // Chama a função para atualizar o gráfico no tema escuro
}

// We handle our user interaction here.
themeSwitch.addEventListener('change', function () {
    if (this.checked) {
        setTheme(0)
        setIndicator(0)
        setPage(0)
    } else {
        setTheme(1)
        setIndicator(1)
        setPage(1)
    }
});
