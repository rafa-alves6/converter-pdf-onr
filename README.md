# Conversor de PDF para TIF (Padrão ONR)

## Sobre o Projeto

Este programa foi desenvolvido para automatizar a conversão de arquivos PDF de matrículas de imóveis para o formato TIFF, seguindo as especificações técnicas do ONR (Operador Nacional do Sistema de Registro Eletrônico de Imóveis).

O objetivo é simplificar e padronizar o processo de digitalização, criando a estrutura de diretórios e a nomenclatura de arquivos exigida de forma automática.

## Funcionalidades

* **Conversão para TIFF:** Transforma PDFs em arquivos TIFF com 200 DPI, em preto-e-branco e com compressão LZW para otimização de tamanho.
* **Estrutura de Diretórios Automática:** Cria a estrutura de pastas com 6 ou 8 dígitos, conforme a necessidade.
* **Nomenclatura Inteligente:** Renomeia os arquivos de saída para o padrão especificado pelo ONR, além do padrão alternativo de número 11, conforme [manual de distribuição de matrículas do ONR](https://www.registrodeimoveis.org.br/intranet/arquivos/upload/geral/instrucaoes_envio__imagens_livro_2.pdf).
* **Incremento de Páginas:** Se uma matrícula já existe na pasta de destino, o programa continua a numeração das páginas, evitando a sobreposição de arquivos.
* **Interface Gráfica Simples:** Uma GUI intuitiva que guia o usuário em 3 passos simples: selecionar PDFs, escolher o destino e converter.

## 📥 Download e Instalação

A versão mais recente do programa pode ser baixada diretamente da nossa página de **Releases**.

**[➡️ Baixar a Versão Mais Recente (v1.8)](https://github.com/rafa-alves6/converter-pdf-onr/releases/latest)**

O download é um único arquivo `setup.exe` que instalará o programa e todas as dependências necessárias (ImageMagick e Ghostscript). Durante a instalação, o assistente irá guiar você na instalação das dependências.

**Importante:** Na tela de instalação do ImageMagick, certifique-se de que a opção **"Add application directory to your system path (PATH)"** esteja marcada.

## 🛠️ Como Usar

1.  **Selecione os Arquivos PDF:** Clique no primeiro botão e escolha um ou mais arquivos PDF para conversão.
2.  **Selecione a Pasta de Destino:** Clique no segundo botão e escolha onde a estrutura de pastas e os arquivos TIFF serão salvos.
3.  **Escolha a Estrutura:** Selecione o formato de 8 ou 6 dígitos no menu dropdown.
4.  **Inicie a Conversão:** Clique no botão verde para começar o processo.

Ao final, um relatório informará sobre o sucesso da operação ou qualquer aviso relevante.

## 📜 Licença

Este programa é um software livre: você pode redistribuí-lo e/ou modificá-lo sob os termos da **GNU Affero General Public License** como publicada pela Free Software Foundation, seja a versão 3 da Licença, ou (a seu critério) qualquer versão posterior.

Este programa é distribuído na esperança de que seja útil, mas SEM QUALQUER GARANTIA; sem mesmo a garantia implícita de COMERCIALIZAÇÃO ou ADEQUAÇÃO A UM DETERMINADO FIM. Veja a GNU Affero General Public License para mais detalhes.

Você deve ter recebido uma cópia da GNU Affero General Public License junto com este programa. Se não, veja [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).

Adicionalmente, este programa utiliza as seguintes bibliotecas de terceiros, que são distribuídas sob suas próprias licenças:
* **ImageMagick:** [Licença do ImageMagick](https://imagemagick.org/script/license.php)
* **Ghostscript:** [Licença AGPL](https://artifex.com/licensing/gnu-agpl-v3)
