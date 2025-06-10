# seu_projeto/schemas/schemas.py (Exemplo de conteúdo)

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

# --- Schemas de Despesa (já devem estar aqui) ---
class DespesaInputSchema(BaseModel):
    nome_despesa: str = Field(..., description="Nome da despesa")
    valor: float = Field(..., description="Valor da despesa")
    data_despesa: Optional[date] = Field(None, description="Data da despesa (YYYY-MM-DD)")
    data_vencimento_mensal: date = Field(..., description="Data de vencimento mensal (YYYY-MM-DD)")
    categoria_id: int = Field(..., description="ID da categoria associada")

class DespesaViewSchema(BaseModel):
    id: int
    nome_despesa: str
    valor: float
    data_despesa: Optional[date]
    data_vencimento_mensal: date
    cadastrado_em: datetime
    categoria_id: int # É bom incluir o ID da categoria na view de despesa

    class Config:
        from_attributes = True

class ListagemDespesasSchema(BaseModel):
    despesas: List[DespesaViewSchema]

# --- Schemas Genéricos (já devem estar aqui) ---
class ErrorSchema(BaseModel):
    message: str

# Schema para buscar Despesa por ID (se você o tiver)
class DespesaBuscaIdSchema(BaseModel):
    id: int = Field(..., description="ID da despesa")

# --- ADICIONE OS SCHEMAS DE CATEGORIA AQUI ---
class CategoriaInputSchema(BaseModel):
    nome: str = Field(..., description="Nome da categoria")

class CategoriaViewSchema(BaseModel):
    id: int
    nome: str
    cadastrado_em: datetime

    class Config:
        from_attributes = True

class ListagemCategoriasSchema(BaseModel):
    categorias: List[CategoriaViewSchema]

# Schema para buscar Categoria por ID
class CategoriaBuscaIdSchema(BaseModel):
    id: int = Field(..., description="ID da categoria")