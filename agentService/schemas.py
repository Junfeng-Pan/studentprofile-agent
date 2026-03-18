from pydantic import BaseModel, Field
from typing import List

class Skill(BaseModel):
    name: str = Field(..., description="技能名称，例如：SpringBoot, MySQL")
    level: int = Field(default=1, ge=1, le=5, description="熟练度评分，范围1~5，1=入门，5=精通")
    evidence: str = Field(default="", description="简历中支撑该技能的原文，精准截取")

class Certificate(BaseModel):
    name: str = Field(..., description="证书名称，例如：英语六级")
    evidence: str = Field(default="", description="简历中支撑该证书的原文，精准截取")

class ExperienceItem(BaseModel):
    name: str = Field(..., description="项目或者实习经历的名称")
    evidence: str = Field(default="", description="简历中支撑该经历的原文描述")

class ScoreLevel(BaseModel):
    level: int = Field(default=1, ge=1, le=5, description="评分，范围1~5")

class StudentProfile(BaseModel):
    """提取的学生简历结构化信息"""
    skills: List[Skill] = Field(default_factory=list, description="提取学生技能和熟练度评分")
    certificates: List[Certificate] = Field(default_factory=list, description="提取学生相关证书")
    Experience: List[ExperienceItem] = Field(default_factory=list, description="提取项目经历与实习经历信息")
    Professionalism: ScoreLevel = Field(default_factory=lambda: ScoreLevel(level=1), description="根据简历的信息判断职业素养评分，范围1~5")
    Potential: ScoreLevel = Field(default_factory=lambda: ScoreLevel(level=1), description="根据简历信息判断发展潜力评分，范围1~5")
