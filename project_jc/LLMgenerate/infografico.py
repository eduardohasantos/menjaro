#from diffusers import StableDiffusionPipeline
from transformers import pipeline
from app1.models import Noticia 
from app1.models import Resumo


class LLMclass:

    #prompt de exemplo
    prompt = """ 
        Em matemática, um grupo é um conjunto de elementos associados a uma operação que combina dois elementos quaisquer para formar um terceiro. Para se qualificar como grupo o conjunto e a operação devem satisfazer algumas condições chamadas axiomas de grupo: associatividade, elemento neutro e elementos inversos. Apesar destes serem comuns a muitas estruturas matemáticas familiares - e.g. os números inteiros munidos da adição formam um grupo - a formulação dos axiomas é independente da natureza concreta do grupo e sua operação. Isso permite lidar-se com entidade de origens matemáticas completamente diferentes de uma maneira flexível, mas retendo os aspectos estruturais essenciais de muitos objetos da álgebra abstrata e além. A ubiquidade dos grupos em inúmeras áreas - dentro e fora da matemática - os tornam um princípio organizador central da matemática contemporânea.
        
        """
        
    def geraResumo(self, prompt:str, obj:Noticia):
        pipe = pipeline("summarization", model="facebook/bart-large-cnn", device="cuda") # Para usar a GPU no processamento

        resultado = pipe(prompt, max_length=400, min_length=30) #Porque não pegar o indice 2 para pegar o resumo??
        self.registraResumo(resultado, obj)
        
        print(resultado)
        
    def registraResumo(self, resultado:list, obj:Noticia):
        textoResultado = resultado[0].get("summary_text")
        
        resumoTxt = Resumo(textoResumo=textoResultado, noticiaRelacionada=obj)
        resumoTxt.save()
        
    #=====================================TESTE============================================
    
    def funcaoTesteResumo(prompt=prompt): 
        pipe = pipeline("summarization", model="facebook/bart-large-cnn", device="cuda") # Para usar a GPU no processamento

        resultado = pipe(prompt, max_length=130, min_length=30)
        print(resultado)
    
    #========================================================DESCONTINUADA===============================================================    
    imagePath = "menjaro/project_jc/media/noticias"
    
    # def funcaoTesteInfografico():
    #     model_id = "sd-legacy/stable-diffusion-v1-5" 
    #     pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32, safety_checker = None)
    #     pipe=pipe.to("cuda")
        
    #     prompt = "An infographic with data about a ficctional city"
    #     image = pipe(prompt).images[0]
        
    #     image.save("infográfico_de_teste.png")
        
    # def geraInfografico(prompt:str, destino:str,nome:str):
    #     pass
        
    #     #LLM pega o prompt
    #     #gera o infográfico
