import os
import datetime
from github import Github, GithubException
from dateutil import easter

def get_readme_filename():
    """Determina qual arquivo de README usar com base no mês atual."""
    
    today = datetime.date.today()
    current_month = today.month
    
    # Calcula a data da Páscoa para o ano atual
    easter_date = easter.easter(today.year)
    
    # Mapa dos meses para os arquivos de README
    readme_map = {
        1: "readme_ano_novo.md",
        2: "readme_valentine's Day.md",
        3: "readme_patrick's day.md",
        6: "readme_valentine's Day.md", # Dia dos Namorados
        10: "readme_hallowen.md",
        12: "readme_natal.md"
    }
    
    # Caso especial para a Páscoa, que não tem mês fixo
    if current_month == easter_date.month:
        return "readme_Easter.md"
        
    # Retorna o README do mapa ou o normal se não houver data especial
    return readme_map.get(current_month, "readme_normal.md")

def main():
    try:
        # Pega as variáveis de ambiente necessárias para a automação
        github_token = os.environ['GITHUB_TOKEN']
        repo_name = os.environ['GITHUB_REPOSITORY'] # Ex: 'SeuUsuario/SeuUsuario'

        # Autentica na API do GitHub
        g = Github(github_token)
        repo = g.get_repo(repo_name)

        source_filename = get_readme_filename()
        
        print(f"Data de hoje: {datetime.date.today()}. Usando o arquivo: {source_filename}")

        # Lê o conteúdo do arquivo de origem (ex: readme_natal.md)
        with open(source_filename, 'r', encoding='utf-8') as file:
            new_content = file.read()

        # Pega o conteúdo do README.md atual no repositório
        try:
            target_file = repo.get_contents("README.md")
            current_content_decoded = target_file.decoded_content.decode('utf-8')

            # Se o conteúdo já for o mesmo, não faz nada para evitar commits desnecessários
            if current_content_decoded == new_content:
                print("O README.md já está atualizado. Nenhuma ação necessária.")
                return
        except GithubException as e:
            if e.status == 404:
                # Se o README.md não existir, cria ele
                target_file = None
                print("README.md não encontrado, será criado.")
            else:
                raise

        # Se houver mudança, atualiza o arquivo README.md
        commit_message = f"🎉 Atualiza README para {source_filename}"
        
        if target_file:
            # Atualiza o arquivo existente
            repo.update_file(
                path=target_file.path,
                message=commit_message,
                content=new_content,
                sha=target_file.sha
            )
        else:
            # Cria o arquivo se ele não existir
            repo.create_file(
                path="README.md",
                message=commit_message,
                content=new_content
            )

        print(f"✅ README.md atualizado com sucesso para '{source_filename}'!")

    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")
        exit(1)

if __name__ == "__main__":
    main()