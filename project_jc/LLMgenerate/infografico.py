from transformers import pipeline
from diffusers import StableDiffusionPipeline
from project_jc.app1.models import Noticia 
from project_jc.app1.models import resumo
import torch


class infografico:

    # Função temporária para teste
    imagePath = "menjaro/project_jc/media/noticias"

    prompt = """ 
        Em matemática, um grupo é um conjunto de elementos associados a uma operação que combina dois elementos quaisquer para formar um terceiro. Para se qualificar como grupo o conjunto e a operação devem satisfazer algumas condições chamadas axiomas de grupo: associatividade, elemento neutro e elementos inversos. Apesar destes serem comuns a muitas estruturas matemáticas familiares - e.g. os números inteiros munidos da adição formam um grupo - a formulação dos axiomas é independente da natureza concreta do grupo e sua operação. Isso permite lidar-se com entidade de origens matemáticas completamente diferentes de uma maneira flexível, mas retendo os aspectos estruturais essenciais de muitos objetos da álgebra abstrata e além. A ubiquidade dos grupos em inúmeras áreas - dentro e fora da matemática - os tornam um princípio organizador central da matemática contemporânea.
        
        """

    def funcaoTesteResumo(prompt=prompt): 
        pipe = pipeline("summarization", model="facebook/bart-large-cnn", device="cuda") # Para usar a GPU no processamento

        resultado = pipe(prompt, max_length=130, min_length=30)
        print(resultado)
    
    def funcaoTesteInfografico():
        model_id = "sd-legacy/stable-diffusion-v1-5" 
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32, safety_checker = None)
        pipe=pipe.to("cuda")
        
        prompt = "An infographic with data about a ficctional city"
        image = pipe(prompt).images[0]
        
        image.save("infográfico_de_teste.png")
    # Fim da função
        
    def geraInfografico(prompt:str, destino:str,nome:str):
        pass
        
        #LLM pega o prompt
        #gera o infográfico
     
    def geraResumo(obj : Noticia):
        pipe = pipeline("summarization", model="facebook/bart-large-cnn", device="cuda") # Para usar a GPU no processamento

        resultado = pipe(obj.conteudo, max_length=130, min_length=30) #Porque não pegar o indice 2 para pegar o resumo??
        resumoTxt = resumo(textoResumo=resultado, noticiaRelacionada=obj)
        resumoTxt.save()
        
        print(resultado)
    
    def registroResumo():
        pass
    
    def registroInfografico():
        pass

if __name__ == "__main__":
    infografico.funcaoTesteInfografico()