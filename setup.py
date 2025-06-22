"""
Script de setup para o APP_AGENTES
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def create_virtual_environment():
    """Cria o ambiente virtual"""
    if os.path.exists("venv"):
        print("✅ Ambiente virtual já existe")
        return True
    
    print("🔧 Criando ambiente virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao criar ambiente virtual")
        return False

def install_dependencies():
    """Instala as dependências"""
    print("📦 Instalando dependências...")
    
    # Determinar o comando pip correto
    if os.name == 'nt':  # Windows
        pip_cmd = os.path.join("venv", "Scripts", "pip")
    else:  # Unix/Linux/Mac
        pip_cmd = os.path.join("venv", "bin", "pip")
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_env_file():
    """Cria o arquivo .env se não existir"""
    if os.path.exists(".env"):
        print("✅ Arquivo .env já existe")
        return True
    
    if os.path.exists("env_template.txt"):
        try:
            shutil.copy("env_template.txt", ".env")
            print("✅ Arquivo .env criado a partir do template")
            print("⚠️  Lembre-se de configurar suas chaves de API no arquivo .env")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar arquivo .env: {e}")
            return False
    else:
        print("❌ Template env_template.txt não encontrado")
        return False

def main():
    """Função principal do setup"""
    print("🚀 Setup do APP_AGENTES")
    print("=" * 50)
    
    # Verificar versão do Python
    if not check_python_version():
        return False
    
    # Criar ambiente virtual
    if not create_virtual_environment():
        return False
    
    # Instalar dependências
    if not install_dependencies():
        return False
    
    # Criar arquivo .env
    if not create_env_file():
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure suas chaves de API no arquivo .env")
    print("2. Ative o ambiente virtual:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source venv/bin/activate")
    print("3. Execute a aplicação:")
    print("   streamlit run app/main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 