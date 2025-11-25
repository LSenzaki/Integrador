# 🎨 GUIA DE ESTUDO - FRONTEND E DOCUMENTAÇÃO (Arthur)

## 📋 Índice
1. [Visão Geral do Frontend](#visão-geral-do-frontend)
2. [Arquitetura React](#arquitetura-react)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Componentes Principais](#componentes-principais)
5. [Hooks Customizados](#hooks-customizados)
6. [Integração com API](#integração-com-api)
7. [Estilização com Tailwind CSS](#estilização-com-tailwind-css)
8. [Captura de Webcam](#captura-de-webcam)
9. [Sistema de Documentação](#sistema-de-documentação)
10. [MkDocs e Material Theme](#mkdocs-e-material-theme)

---

## 🎯 Visão Geral do Frontend

O frontend foi desenvolvido com **React**, uma biblioteca JavaScript para construir interfaces de usuário, usando **Tailwind CSS** para estilização moderna e responsiva.

### Arquitetura da Aplicação

```
┌─────────────────────────────────────┐
│       BROWSER (Cliente)             │
│                                     │
│  ┌───────────────────────────────┐ │
│  │     React Application         │ │
│  │  ┌─────────────────────────┐  │ │
│  │  │   Components (UI)       │  │ │
│  │  ├─────────────────────────┤  │ │
│  │  │   Hooks (Lógica)        │  │ │
│  │  ├─────────────────────────┤  │ │
│  │  │   API Client (Fetch)    │  │ │
│  │  └─────────────────────────┘  │ │
│  └───────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │ HTTP Requests
               │ (GET, POST, PUT, DELETE)
               ▼
┌─────────────────────────────────────┐
│     Backend API (FastAPI)           │
│     http://localhost:8000           │
└─────────────────────────────────────┘
```

### Princípios de Design

1. **Component-Based**: Interface dividida em componentes reutilizáveis
2. **State Management**: Gerenciamento de estado com React Hooks
3. **Responsive Design**: Funciona em desktop, tablet e mobile
4. **User Experience**: Feedback visual e mensagens claras
5. **Performance**: Otimizações de renderização

---

## ⚛️ Arquitetura React

### O que é React?

**React** é uma biblioteca JavaScript para construir interfaces de usuário baseadas em **componentes**.

**Conceitos Fundamentais:**

1. **Componentes**: Blocos reutilizáveis de UI
2. **Props**: Dados passados de pai para filho
3. **State**: Dados que mudam ao longo do tempo
4. **Hooks**: Funções que permitem usar state e outros recursos
5. **Virtual DOM**: Representação em memória do DOM real (performance)

### JSX (JavaScript XML)

JSX permite escrever HTML dentro do JavaScript:

```jsx
// JSX - Parece HTML
const elemento = <h1>Olá, Mundo!</h1>;

// É transformado em JavaScript
const elemento = React.createElement('h1', null, 'Olá, Mundo!');
```

**Vantagens:**
- ✅ Sintaxe familiar (HTML-like)
- ✅ Type checking
- ✅ Expressões JavaScript inline

### Componentes Funcionais

```jsx
// Componente simples
function Saudacao() {
  return <h1>Olá!</h1>;
}

// Componente com props
function SaudacaoPersonalizada({ nome }) {
  return <h1>Olá, {nome}!</h1>;
}

// Uso
<SaudacaoPersonalizada nome="Arthur" />
```

### React Hooks

**Hooks** são funções que permitem usar recursos do React em componentes funcionais.

**Principais Hooks:**

1. **useState**: Gerenciar estado
2. **useEffect**: Efeitos colaterais (API calls, subscriptions)
3. **useRef**: Referência a elementos DOM
4. **useCallback**: Memoização de funções
5. **useMemo**: Memoização de valores

---

## 📁 Estrutura do Projeto

```
frontend/
├── public/
│   ├── index.html           # HTML base
│   ├── manifest.json        # PWA manifest
│   └── robots.txt           # SEO
│
├── src/
│   ├── index.js             # Entry point
│   ├── index.css            # Estilos globais + Tailwind
│   ├── App.js               # Componente principal (TODOS os componentes)
│   ├── App.css              # Estilos do App
│   │
│   ├── components/          # Componentes reutilizáveis
│   │   └── student/
│   │       ├── index.js
│   │       └── SelecionarTurma.jsx
│   │
│   ├── pages/               # Páginas/telas
│   │   ├── index.js
│   │   └── AlunoScreen.jsx
│   │
│   ├── hooks/               # Custom hooks
│   │   ├── index.js
│   │   └── useWebcam.js
│   │
│   ├── constants/           # Constantes (API URL)
│   │   ├── index.js
│   │   └── api.js
│   │
│   └── utils/               # Funções utilitárias
│       ├── index.js
│       └── helpers.js
│
├── package.json             # Dependências e scripts
├── tailwind.config.js       # Configuração Tailwind
└── postcss.config.js        # PostCSS config
```

### Arquivos Principais

**1. index.js** (Entry Point)
```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**2. App.js** (Componente Principal)
```jsx
import React, { useState } from 'react';
import './App.css';

function App() {
  const [telaAtual, setTelaAtual] = useState('home');
  
  return (
    <div className="App">
      {telaAtual === 'home' && <Home />}
      {telaAtual === 'aluno' && <AlunoScreen />}
      {/* Outras telas... */}
    </div>
  );
}

export default App;
```

**3. package.json** (Dependências)
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "dependencies": {
    "react": "^19.2.0",           // Biblioteca React
    "react-dom": "^19.2.0",       // React para web
    "react-scripts": "5.0.1",     // Scripts CRA
    "lucide-react": "^0.552.0",   // Ícones
    "tailwindcss": "^3.4.18"      // CSS utility-first
  },
  "scripts": {
    "start": "react-scripts start",    // Dev server
    "build": "react-scripts build",    // Build produção
    "test": "react-scripts test"       // Testes
  }
}
```

---

## 🧩 Componentes Principais

### 1. Home Screen

```jsx
function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold text-white text-center mb-12">
          Sistema de Chamada Automática
        </h1>
        
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {/* Card Aluno */}
          <button 
            onClick={() => setTelaAtual('aluno')}
            className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition-all"
          >
            <Camera className="w-16 h-16 mx-auto text-blue-500 mb-4" />
            <h2 className="text-2xl font-bold text-gray-800">
              Chamada
            </h2>
            <p className="text-gray-600 mt-2">
              Reconhecimento facial para presença
            </p>
          </button>
          
          {/* Card Gestão */}
          <button className="bg-white p-8 rounded-xl...">
            {/* Similar para outras telas */}
          </button>
        </div>
      </div>
    </div>
  );
}
```

**Conceitos:**
- **Conditional Rendering**: `{telaAtual === 'home' && <Home />}`
- **Event Handlers**: `onClick={() => setTelaAtual('aluno')}`
- **Tailwind Classes**: `bg-white p-8 rounded-xl shadow-lg`

### 2. AlunoScreen (Reconhecimento)

```jsx
import React, { useState } from 'react';
import SelecionarTurma from '../components/student/SelecionarTurma';
import TelaReconhecimento from '../components/student/TelaReconhecimento';

function AlunoScreen() {
  const [turmaSelecionada, setTurmaSelecionada] = useState(null);
  const [chamadaIniciada, setChamadaIniciada] = useState(false);

  // Se não iniciou, mostra seleção de turma
  if (!chamadaIniciada) {
    return (
      <SelecionarTurma
        setTurmaSelecionada={setTurmaSelecionada}
        setChamadaIniciada={setChamadaIniciada}
      />
    );
  }

  // Se iniciou, mostra tela de reconhecimento
  return (
    <TelaReconhecimento
      turma={turmaSelecionada}
      setChamadaIniciada={setChamadaIniciada}
    />
  );
}

export default AlunoScreen;
```

**Padrão de Composição:**
```
AlunoScreen (Container)
├── SelecionarTurma (Step 1)
└── TelaReconhecimento (Step 2)
```

### 3. SelecionarTurma Component

```jsx
import React, { useState, useEffect } from 'react';
import { BookOpen, Search } from 'lucide-react';

const SelecionarTurma = ({ setTurmaSelecionada, setChamadaIniciada }) => {
  // Estados
  const [turmas, setTurmas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState('');

  // Carregar turmas ao montar componente
  useEffect(() => {
    carregarTurmas();
  }, []);

  const carregarTurmas = async () => {
    try {
      const response = await fetch('http://localhost:8000/turmas/');
      const data = await response.json();
      setTurmas(data);
    } catch (err) {
      alert('Erro ao carregar turmas: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const iniciarChamada = (turma) => {
    setTurmaSelecionada(turma);
    setChamadaIniciada(true);
  };

  // Filtrar turmas pela busca
  const turmasFiltradas = turmas.filter(turma => 
    turma.nome.toLowerCase().includes(busca.toLowerCase())
  );

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <BookOpen className="w-6 h-6" />
          Iniciar Chamada - Selecione a Turma
        </h2>

        {/* Campo de busca */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar turma..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
            />
          </div>
        </div>

        {/* Lista de turmas */}
        {loading ? (
          <p className="text-center py-8 text-gray-500">Carregando turmas...</p>
        ) : turmasFiltradas.length === 0 ? (
          <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg">
            <p className="font-semibold">Nenhuma turma encontrada</p>
          </div>
        ) : (
          <div className="grid gap-3 max-h-[500px] overflow-y-auto">
            {turmasFiltradas.map(turma => (
              <button
                key={turma.id}
                onClick={() => iniciarChamada(turma)}
                className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all text-left group"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-gray-800 group-hover:text-blue-600">
                      {turma.nome}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      ID: {turma.id}
                    </p>
                  </div>
                  <div className="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">
                    →
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SelecionarTurma;
```

**Conceitos React:**
- **useState**: Gerenciar turmas, loading, busca
- **useEffect**: Carregar dados ao montar
- **Props**: Receber setters do componente pai
- **Controlled Input**: `value={busca} onChange={...}`
- **Conditional Rendering**: Loading / Empty / List
- **Array methods**: `filter()`, `map()`

### 4. TelaReconhecimento Component

```jsx
import React, { useRef, useState, useEffect } from 'react';
import { Camera, Video, VideoOff } from 'lucide-react';

const TelaReconhecimento = ({ turma, setChamadaIniciada }) => {
  // Refs para acessar elementos DOM
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Estados
  const [streaming, setStreaming] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);

  // Controlar webcam baseado no estado streaming
  useEffect(() => {
    if (streaming) {
      startCamera();
    } else {
      stopCamera();
    }
    
    // Cleanup: parar câmera ao desmontar
    return () => stopCamera();
  }, [streaming]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'user', width: 640, height: 480 }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      alert('Erro ao acessar câmera: ' + err.message);
      setStreaming(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const capturarEReconhecer = async () => {
    if (!videoRef.current) return;
    
    // Capturar frame do vídeo
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    // Converter para Blob
    canvas.toBlob(async (blob) => {
      setLoading(true);
      
      const formData = new FormData();
      formData.append('foto', blob, 'captura.jpg');
      formData.append('turma_id', turma.id);

      try {
        const response = await fetch('http://localhost:8000/alunos/reconhecer', {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        setResultado(data);
      } catch (err) {
        alert('Erro ao reconhecer: ' + err.message);
      } finally {
        setLoading(false);
      }
    });
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        {/* Header */}
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Camera className="w-6 h-6" />
              Reconhecimento de Presença
            </h2>
            <div className="mt-2 p-3 bg-blue-50 border-2 border-blue-200 rounded-lg">
              <p className="text-sm text-blue-600">
                <span className="font-semibold">Turma:</span> {turma.nome}
              </p>
            </div>
          </div>
          <button
            onClick={() => {
              stopCamera();
              setChamadaIniciada(false);
            }}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-semibold transition-colors"
          >
            ← Trocar Turma
          </button>
        </div>

        {/* Vídeo da webcam */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video mb-4">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className={`w-full h-full object-cover ${!streaming && 'hidden'}`}
          />
          <canvas ref={canvasRef} className="hidden" />
          
          {!streaming && (
            <div className="absolute inset-0 flex items-center justify-center">
              <VideoOff className="w-16 h-16 text-gray-500" />
            </div>
          )}
        </div>

        {/* Controles */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setStreaming(!streaming)}
            className={`flex-1 py-3 rounded-lg font-semibold transition-colors ${
              streaming
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-green-500 hover:bg-green-600 text-white'
            }`}
          >
            {streaming ? (
              <>
                <VideoOff className="inline w-5 h-5 mr-2" />
                Parar Câmera
              </>
            ) : (
              <>
                <Video className="inline w-5 h-5 mr-2" />
                Iniciar Câmera
              </>
            )}
          </button>
          
          <button
            onClick={capturarEReconhecer}
            disabled={!streaming || loading}
            className="flex-1 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg font-semibold transition-colors"
          >
            {loading ? 'Reconhecendo...' : 'Capturar e Reconhecer'}
          </button>
        </div>

        {/* Resultado */}
        {resultado && (
          <div className={`p-4 rounded-lg ${
            resultado.status === 'success' 
              ? 'bg-green-50 border-2 border-green-500' 
              : 'bg-red-50 border-2 border-red-500'
          }`}>
            <h3 className="font-bold text-lg mb-2">
              {resultado.status === 'success' ? '✅ Reconhecido!' : '❌ Não Reconhecido'}
            </h3>
            <p>{resultado.message}</p>
            {resultado.confidence && (
              <p className="text-sm mt-2">
                Confiança: {resultado.confidence.toFixed(1)}%
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TelaReconhecimento;
```

**Conceitos Avançados:**
- **useRef**: Acessar elementos DOM (video, canvas)
- **MediaDevices API**: `getUserMedia()` para webcam
- **Canvas API**: Capturar frame do vídeo
- **Blob API**: Converter imagem para arquivo
- **FormData**: Enviar arquivo via POST
- **Cleanup**: `return () => stopCamera()` no useEffect

---

## 🪝 Hooks Customizados

### useWebcam Hook

Encapsula lógica de webcam em um hook reutilizável:

```jsx
// hooks/useWebcam.js
import { useState, useRef, useCallback } from 'react';

export const useWebcam = () => {
  const [webcamAtiva, setWebcamAtiva] = useState(false);
  const [erro, setErro] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const iniciarWebcam = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: 640, height: 480 }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setWebcamAtiva(true);
        setErro(null);
      }
    } catch (err) {
      console.error('Erro ao acessar webcam:', err);
      setErro('Erro ao acessar a webcam. Verifique as permissões.');
      setWebcamAtiva(false);
    }
  }, []);

  const pararWebcam = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setWebcamAtiva(false);
  }, []);

  return {
    videoRef,
    webcamAtiva,
    erro,
    iniciarWebcam,
    pararWebcam
  };
};
```

**Uso:**
```jsx
function MeuComponente() {
  const { videoRef, webcamAtiva, erro, iniciarWebcam, pararWebcam } = useWebcam();
  
  return (
    <div>
      <video ref={videoRef} autoPlay />
      <button onClick={webcamAtiva ? pararWebcam : iniciarWebcam}>
        {webcamAtiva ? 'Parar' : 'Iniciar'}
      </button>
      {erro && <p>{erro}</p>}
    </div>
  );
}
```

**Vantagens de Custom Hooks:**
- ✅ Reutilização de lógica
- ✅ Código mais limpo
- ✅ Separação de responsabilidades
- ✅ Facilita testes

---

## 🔌 Integração com API

### Configuração da API

```javascript
// constants/api.js
export const API_URL = 'http://localhost:8000';

// constants/index.js
export { API_URL } from './api';
```

### Padrões de Requisição

**1. GET - Listar Dados**
```javascript
const listarTurmas = async () => {
  try {
    const response = await fetch(`${API_URL}/turmas/`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    setTurmas(data);
  } catch (error) {
    console.error('Erro ao listar turmas:', error);
    alert('Erro ao carregar turmas');
  }
};
```

**2. POST - Criar/Enviar Dados**
```javascript
const cadastrarAluno = async (nome, turmaId, fotos) => {
  const formData = new FormData();
  formData.append('nome', nome);
  formData.append('turma_id', turmaId);
  
  // Adicionar múltiplas fotos
  fotos.forEach((foto, index) => {
    formData.append('fotos', foto, `foto_${index}.jpg`);
  });

  try {
    const response = await fetch(`${API_URL}/alunos/cadastrar`, {
      method: 'POST',
      body: formData  // Não definir Content-Type! FormData faz automaticamente
    });

    const data = await response.json();
    
    if (data.status === 'success') {
      alert('Aluno cadastrado com sucesso!');
    }
  } catch (error) {
    console.error('Erro ao cadastrar:', error);
  }
};
```

**3. PUT - Atualizar Dados**
```javascript
const atualizarAluno = async (alunoId, dadosNovos) => {
  try {
    const response = await fetch(`${API_URL}/alunos/${alunoId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dadosNovos)
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao atualizar:', error);
  }
};
```

**4. DELETE - Deletar Dados**
```javascript
const deletarAluno = async (alunoId) => {
  if (!confirm('Tem certeza que deseja deletar?')) return;

  try {
    const response = await fetch(`${API_URL}/alunos/${alunoId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      alert('Aluno deletado com sucesso!');
      // Recarregar lista
      listarAlunos();
    }
  } catch (error) {
    console.error('Erro ao deletar:', error);
  }
};
```

### Tratamento de Erros

```javascript
const fetchComTratamento = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    
    // Verificar status HTTP
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    // Erro de rede
    if (error instanceof TypeError) {
      alert('Erro de conexão. Verifique sua internet.');
    } 
    // Erro do servidor
    else {
      alert(`Erro: ${error.message}`);
    }
    
    console.error('Fetch error:', error);
    throw error;
  }
};
```

---

## 🎨 Estilização com Tailwind CSS

### O que é Tailwind CSS?

**Tailwind** é um framework CSS **utility-first**: em vez de escrever CSS customizado, você aplica classes utilitárias diretamente no HTML/JSX.

### Configuração

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",  // Onde procurar classes
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
      },
    },
  },
  plugins: [],
};
```

```css
/* index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Classes Principais

**Layout:**
```jsx
<div className="container mx-auto px-4">     {/* Container centralizado */}
<div className="flex items-center justify-between"> {/* Flexbox */}
<div className="grid grid-cols-3 gap-4">    {/* Grid */}
```

**Spacing (Margin/Padding):**
```jsx
<div className="p-4">      {/* padding: 1rem (16px) */}
<div className="m-6">      {/* margin: 1.5rem (24px) */}
<div className="px-8 py-2"> {/* padding-x: 2rem, padding-y: 0.5rem */}
<div className="mt-4 mb-2"> {/* margin-top: 1rem, margin-bottom: 0.5rem */}
```

**Typography:**
```jsx
<h1 className="text-4xl font-bold text-gray-800">
<p className="text-sm text-gray-600 leading-relaxed">
<span className="font-semibold uppercase tracking-wide">
```

**Colors:**
```jsx
<div className="bg-blue-500 text-white">        {/* Background + Text */}
<div className="bg-gray-100 border-2 border-gray-300"> {/* Border */}
<div className="hover:bg-blue-600">             {/* Hover state */}
```

**Border & Rounded:**
```jsx
<div className="rounded-lg border-2 shadow-lg">
<button className="rounded-full">  {/* Círculo */}
```

**Responsive Design:**
```jsx
<div className="w-full md:w-1/2 lg:w-1/3">
{/* 
  w-full: 100% em mobile
  md:w-1/2: 50% em tablets (768px+)
  lg:w-1/3: 33% em desktop (1024px+)
*/}
```

**States:**
```jsx
<button className="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 disabled:bg-gray-300">
```

### Exemplo Completo

```jsx
<div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 p-8">
  <div className="max-w-4xl mx-auto">
    <div className="bg-white rounded-xl shadow-2xl p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Título
      </h1>
      
      <div className="grid md:grid-cols-2 gap-4">
        <button className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105">
          Botão 1
        </button>
        
        <button className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105">
          Botão 2
        </button>
      </div>
    </div>
  </div>
</div>
```

---

## 📸 Captura de Webcam

### MediaDevices API

```javascript
// Pedir permissão e iniciar webcam
const iniciarWebcam = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'user',  // Câmera frontal
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    });
    
    videoElement.srcObject = stream;
  } catch (error) {
    if (error.name === 'NotAllowedError') {
      alert('Permissão negada para acessar câmera');
    } else if (error.name === 'NotFoundError') {
      alert('Nenhuma câmera encontrada');
    }
  }
};
```

### Canvas para Captura

```javascript
const capturarFrame = () => {
  const canvas = document.createElement('canvas');
  const video = videoRef.current;
  
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);
  
  // Converter para Blob
  canvas.toBlob((blob) => {
    // blob contém a imagem capturada
    enviarParaAPI(blob);
  }, 'image/jpeg', 0.95);  // JPEG com 95% qualidade
};
```

### Enviar para API

```javascript
const enviarParaAPI = async (imageBlob) => {
  const formData = new FormData();
  formData.append('foto', imageBlob, 'captura.jpg');
  formData.append('turma_id', turmaId);

  const response = await fetch(`${API_URL}/alunos/reconhecer`, {
    method: 'POST',
    body: formData
  });

  const resultado = await response.json();
  exibirResultado(resultado);
};
```

### Parar Webcam (Importante!)

```javascript
const pararWebcam = () => {
  const video = videoRef.current;
  
  if (video && video.srcObject) {
    // Parar todas as tracks (vídeo/áudio)
    video.srcObject.getTracks().forEach(track => {
      track.stop();
    });
    
    video.srcObject = null;
  }
};

// Cleanup ao desmontar componente
useEffect(() => {
  return () => {
    pararWebcam();
  };
}, []);
```

---

## 📚 Sistema de Documentação

### MkDocs

**MkDocs** é um gerador de sites estáticos focado em documentação técnica.

**Características:**
- ✅ Markdown para conteúdo
- ✅ Temas customizáveis
- ✅ Busca integrada
- ✅ Responsivo
- ✅ Deploy simples

### Estrutura da Documentação

```
docs/
├── index.md                    # Página inicial
├── SENZAKI_BACKEND.md          # Guia do backend
├── KAWAN_COMPARACAO_MODELOS.md # Guia de comparação
├── ARTHUR_FRONTEND_DOCS.md     # Este guia!
│
├── visao-geral/
│   ├── introducao.md
│   ├── arquitetura.md
│   └── tecnologias.md
│
├── instalacao/
│   ├── requisitos.md
│   ├── backend.md
│   ├── frontend.md
│   └── banco-de-dados.md
│
├── api/
│   ├── endpoints.md
│   ├── alunos.md
│   ├── turmas.md
│   ├── professores.md
│   └── presencas.md
│
├── funcionalidades/
│   ├── alunos.md
│   ├── turmas.md
│   ├── professores.md
│   ├── presencas.md
│   └── reconhecimento.md
│
└── guias/
    ├── teste-reconhecimento.md
    ├── preprocessamento.md
    └── sistema-hibrido.md
```

### mkdocs.yml (Configuração)

```yaml
site_name: Sistema de Reconhecimento Facial - Documentação
site_description: Sistema de controle de presença com reconhecimento facial
site_author: Sistema Integrador

theme:
  name: material
  language: pt-BR
  palette:
    # Modo claro
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Modo escuro
    # Modo escuro
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Modo claro
  
  features:
    - navigation.tabs        # Tabs no topo
    - navigation.sections    # Seções na sidebar
    - navigation.top         # Botão "voltar ao topo"
    - search.suggest         # Sugestões de busca
    - search.highlight       # Destacar resultados
    - content.code.copy      # Copiar código

plugins:
  - search:
      lang: pt

markdown_extensions:
  - pymdownx.highlight:      # Syntax highlighting
      anchor_linenums: true
  - pymdownx.inlinehilite    # Inline code
  - pymdownx.snippets        # Include snippets
  - pymdownx.superfences     # Code fences
  - pymdownx.details         # Collapsible blocks
  - pymdownx.tabbed:         # Tabs
      alternate_style: true
  - admonition               # Callouts (note, warning, etc)
  - tables                   # Markdown tables

nav:
  - Início: index.md
  - Visão Geral:
      - Introdução: visao-geral/introducao.md
      - Arquitetura: visao-geral/arquitetura.md
      - Tecnologias: visao-geral/tecnologias.md
  - Instalação:
      - Requisitos: instalacao/requisitos.md
      - Backend: instalacao/backend.md
      - Frontend: instalacao/frontend.md
      - Banco de Dados: instalacao/banco-de-dados.md
  - API:
      - Endpoints: api/endpoints.md
      - Alunos: api/alunos.md
      - Turmas: api/turmas.md
      - Professores: api/professores.md
      - Presenças: api/presencas.md
  - Guias:
      - Teste de Reconhecimento: guias/teste-reconhecimento.md
      - Sistema Híbrido: guias/sistema-hibrido.md
```

### Material Theme

**Material for MkDocs** é um tema baseado no Material Design do Google.

**Features:**
- Design moderno e limpo
- Modo claro/escuro
- Navegação intuitiva
- Busca poderosa
- Mobile-first
- Syntax highlighting
- Admonitions (callouts)

**Exemplo de Markdown com Admonitions:**

```markdown
!!! note "Nota Importante"
    Este é um bloco de nota destacado.

!!! warning "Atenção"
    Cuidado com este comportamento!

!!! tip "Dica"
    Você sabia que...

!!! danger "Perigo"
    Não faça isto em produção!

??? info "Informação Colapsável"
    Clique para expandir
```

### Como Rodar a Documentação

```bash
# Instalar MkDocs
pip install mkdocs mkdocs-material

# Servir localmente (auto-reload)
mkdocs serve
# Acesse: http://localhost:8000

# Build para produção
mkdocs build
# Gera pasta site/ com HTML estático

# Deploy para GitHub Pages
mkdocs gh-deploy
```

### Estrutura de um Documento

```markdown
# Título Principal

## Seção 1

Texto explicativo com **negrito** e *itálico*.

### Subseção 1.1

Lista não ordenada:
- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2

Lista ordenada:
1. Primeiro passo
2. Segundo passo
3. Terceiro passo

## Seção 2: Código

### Bloco de Código

```python
def exemplo():
    print("Olá, Mundo!")
```

### Código Inline

Use `código inline` para destacar comandos.

## Seção 3: Links e Imagens

[Texto do Link](https://exemplo.com)

![Texto Alternativo](caminho/para/imagem.png)

## Seção 4: Tabelas

| Coluna 1 | Coluna 2 | Coluna 3 |
|----------|----------|----------|
| Valor 1  | Valor 2  | Valor 3  |
| Valor 4  | Valor 5  | Valor 6  |

## Seção 5: Admonitions

!!! tip "Dica"
    Use admonitions para destacar informações importantes.
```

---

## 🎓 Conceitos para Estudar

### 1. **React Fundamentals**
- JSX syntax
- Components (functional vs class)
- Props e State
- Event handling
- Conditional rendering
- Lists e Keys

### 2. **React Hooks**
- useState
- useEffect
- useRef
- useCallback
- useMemo
- Custom Hooks

### 3. **Modern JavaScript (ES6+)**
- Arrow functions
- Destructuring
- Spread/Rest operators
- Template literals
- Async/Await
- Array methods (map, filter, reduce)

### 4. **Web APIs**
- Fetch API
- MediaDevices API
- Canvas API
- Blob API
- FormData API

### 5. **CSS e Tailwind**
- Flexbox
- Grid
- Responsive design
- Utility-first CSS
- Pseudo-classes (:hover, :active)

### 6. **Documentação Técnica**
- Markdown syntax
- MkDocs configuration
- Material Design principles
- Technical writing

---

## ✅ Checklist de Conhecimentos

Após estudar este documento, você deve saber:

- [ ] Explicar a arquitetura do frontend React
- [ ] Criar componentes funcionais com props e state
- [ ] Usar hooks (useState, useEffect, useRef)
- [ ] Fazer requisições HTTP com Fetch API
- [ ] Integrar webcam com MediaDevices API
- [ ] Capturar frames com Canvas
- [ ] Estilizar com Tailwind CSS
- [ ] Criar custom hooks reutilizáveis
- [ ] Estruturar projetos React
- [ ] Configurar e usar MkDocs
- [ ] Escrever documentação técnica em Markdown
- [ ] Customizar Material Theme
- [ ] Deploy de documentação estática

---

## 📚 Recursos de Estudo

### Documentação Oficial:
- **React**: https://react.dev/
- **React Hooks**: https://react.dev/reference/react
- **Tailwind CSS**: https://tailwindcss.com/docs
- **MkDocs**: https://www.mkdocs.org/
- **Material for MkDocs**: https://squidfunk.github.io/mkdocs-material/

### Tutoriais:
- **React para Iniciantes**: https://react.dev/learn
- **Tailwind Play**: https://play.tailwindcss.com/
- **MDN Web APIs**: https://developer.mozilla.org/en-US/docs/Web/API

### Ferramentas:
- **Create React App**: https://create-react-app.dev/
- **Vite** (alternativa moderna): https://vitejs.dev/
- **Lucide Icons**: https://lucide.dev/

---

## 🚀 Como Rodar o Frontend

### 1. Instalação

```bash
# Navegar até o diretório frontend
cd frontend

# Instalar dependências
npm install
```

### 2. Desenvolvimento

```bash
# Iniciar servidor de desenvolvimento
npm start

# Acesse: http://localhost:3000
```

### 3. Build para Produção

```bash
# Criar build otimizado
npm run build

# Gera pasta build/ com arquivos estáticos
```

### 4. Deploy

**Opção 1: Vercel**
```bash
npm install -g vercel
vercel
```

**Opção 2: Netlify**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

**Opção 3: GitHub Pages**
```bash
npm install --save-dev gh-pages

# Adicionar em package.json:
"homepage": "https://seunome.github.io/repositorio",
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}

# Deploy
npm run deploy
```

---

**Autor:** Documentação preparada para Arthur (Frontend e Documentação)  
**Data:** Novembro 2025  
**Versão:** 1.0
