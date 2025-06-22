@echo off
REM ========================================
REM   Agentes de Engenharia da Propor
REM ========================================
REM Propor Engenharia
REM Responsavel Tecnico: Eng. Civil Rodrigo Emanuel Rabello
REM CREA-RS: 167.175-D | CNPJ: 41.556.670/0001-76
REM ========================================

setlocal

REM Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Erro: Ambiente virtual nao encontrado!
    echo Execute: python setup.py
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar se o arquivo .env existe
if not exist ".env" (
    echo Aviso: Arquivo .env nao encontrado!
    echo Copiando template...
    copy env_template.txt .env
    echo.
    echo IMPORTANTE: Configure suas chaves de API no arquivo .env
    echo.
)

REM Menu de opcoes
:MENU
cls
ECHO ========================================
ECHO   Agentes de Engenharia da Propor
ECHO ========================================
ECHO 1. Iniciar aplicacao Streamlit
ECHO 2. Rodar testes de agentes (script)
ECHO 3. Rodar todos os testes (pytest)
ECHO 4. Checar qualidade do codigo (flake8)
ECHO 5. Formatar codigo (black)
ECHO 6. Organizar imports (isort)
ECHO 7. Remover imports/variaveis nao usados (autoflake)
ECHO 8. Sair
ECHO ========================================
set /p option=Escolha uma opcao (1-8): 

if "%option%"=="1" goto RUN_STREAMLIT
if "%option%"=="2" goto RUN_AGENT_TESTS
if "%option%"=="3" goto RUN_PYTEST
if "%option%"=="4" goto RUN_FLAKE8
if "%option%"=="5" goto RUN_BLACK
if "%option%"=="6" goto RUN_ISORT
if "%option%"=="7" goto RUN_AUTOFLAKE
if "%option%"=="8" goto END

goto MENU

:RUN_STREAMLIT
ECHO Iniciando aplicacao Streamlit...
echo.
echo A aplicacao sera aberta em: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar a aplicacao
echo.
set PYTHONPATH=%CD%
streamlit run app/main.py
pause
goto MENU

:RUN_AGENT_TESTS
ECHO Rodando testes de agentes...
set PYTHONPATH=.
python examples/test_agent_creation.py
pause
goto MENU

:RUN_PYTEST
ECHO Rodando todos os testes (pytest)...
set PYTHONPATH=.
pytest tests/
pause
goto MENU

:RUN_FLAKE8
ECHO Checando qualidade do codigo (flake8)...
flake8 .
pause
goto MENU

:RUN_BLACK
ECHO Formatando codigo (black)...
black .
pause
goto MENU

:RUN_ISORT
ECHO Organizando imports (isort)...
isort .
pause
goto MENU

:RUN_AUTOFLAKE
ECHO Removendo imports/variaveis nao usados (autoflake)...
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
pause
goto MENU

:END
ECHO Saindo...
endlocal
exit /b 0 