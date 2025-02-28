import os
import traceback
from typing import Any
from datetime import datetime
from pydantic import BaseModel #data validation and settings management.
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    UploadFile,
    HTTPException,
    File,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from utils.log_utils import ServerLogger
from fastapi.templating import Jinja2Templates
from utils.folder_utils import create_directory
from utils.error_utils import ServerException
from fastapi.staticfiles import StaticFiles



class UserRequest(BaseModel):
    query: str
class GenerateCodeRequest(UserRequest):
    current_code: str
class UserResponse(BaseModel):
    response: str

class ErrorHandle:
    def query_empty(self, query: str) -> None:
        if not query:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Query can not empty",
            )

    def respone_empty(self, respone: str) -> None:
        if not respone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No respone generated"
            )

    def file_unspport(self, support) -> None:
        if not support:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Unsupported file type",
            )

class FastApiInterface:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.router_copilot = APIRouter() 
        self.copilot = CopilotCore()
        self.error = ErrorHandle()
        self.SERVER_LOGGER = ServerLogger()
        self.processed_file_path = ""

        origins = [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]

        ## add in middleware to handle "options" response beside [GET, POST, PUT, DELETE]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.UPLOAD_FROM_CLIENT_DIRECTORY = "./data_storage/eclipse_side/server"
        self.SEND_TO_CLIENT_DIRECTORY = "./data_storage/eclipse_side/client"

        ## define static file directory. example your host: http://localhost:8000 --> static file will be http://localhost:8000/static; used for serving assets like images, CSS files, JavaScript files, etc., that are needed for the frontend of your application.
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        ## create index.html template file at ./templates/index.html folder.
        self.templates = Jinja2Templates(directory="templates")
        ## call function below to run.
        self.init_folder()

        try:
            self.setup_routers()
        except Exception as e:
            raise ServerException(
                f"Set up router API fail, more information see here: {e}"
            )
        
    ## Used to include routes (endpoints) from an APIRouter instance into the main FastAPI application
    def start_routers(self):
        self.app.include_router(self.router_copilot, prefix="/copilot") 
    
    ## generate logs folder.
    def init_folder(self) -> None:
        create_directory(self.UPLOAD_FROM_CLIENT_DIRECTORY)
        create_directory(self.SEND_TO_CLIENT_DIRECTORY)
    
    def ssetup_routers(self) -> None:

        @self.app.get("/")
        async def index(request: Request):
            return self.templates.TemplateResponse(
                "index.html", {"request": request, "message": "Hello, World!"}
            )
        @self.router_copilot.post("/generate_code_api", response_model=UserResponse)
        async def generate_code_api(request: GenerateCodeRequest) -> Any: ## using async to permit system run other task paralel.
            respone = ""
            try:
                self.error.query_empty(request.query)
                respone = self.copilot.generate_code(
                    request.current_code, request.query
                )
                self.error.respone_empty(respone)
            except Exception as e:
                raise ServerException(f"Router _Generate_Code_ fail: {e}")
            finally:
                return UserResponse(response=respone)
        @self.router_copilot.post("/analyze_code_api", response_model=UserResponse)
        async def analyze_code_api(request: UserRequest) -> Any:
            respone = ""
            try:
                self.error.query_empty(request.query)
                respone = self.copilot.analyze_code(request.query)
                self.error.respone_empty(respone)
            except Exception as e:
                raise ServerException(f"Router _Analyze_Code_ fail: {e}")
            finally:
                return UserResponse(response=respone)

        @self.router_copilot.post("/autocomplete_code_api", response_model=UserResponse)
        async def autocomplete_code_api(request: UserRequest) -> Any:
            respone = ""
            try:
                self.error.query_empty(request.query)
                respone = self.copilot.complete_code(request.query)
                self.error.respone_empty(respone)
            except Exception as e:
                raise ServerException(f"Router _Autocomplete_Code_ fail: {e}")
            finally:
                return UserResponse(response=respone)

        @self.router_copilot.post("/chat_code_api", response_model=UserResponse)
        async def chat_code_api(request: UserRequest) -> Any:
            respone = ""
            try:
                self.error.query_empty(request.query)
                respone = self.copilot.chat_generate(request.query)
                self.error.respone_empty(respone)
            except Exception as e:
                raise ServerException(f"Router _Chat_Code_ fail: {e}")
            finally:
                return UserResponse(response=respone)

        @self.router_copilot.post("/comment_code_api", response_model=UserResponse)
        async def comment_code_api(request: UserRequest) -> Any:
            respone = ""
            try:
                self.error.query_empty(request.query)
                respone = self.copilot.comment_code(request.query)
                self.error.respone_empty(respone)
            except Exception as e:
                raise ServerException(f"Router _Comment_Code_ fail: {e}")
            finally:
                return UserResponse(response=respone)

        @self.router_copilot.post("/gen_standard_rule_api")
        async def gen_standard_rule_api(file: UploadFile = File(...)) -> Any:
            self.error.file_unspport(file.filename.endswith(".xlsx"))

            header_code = ""
            source_code = ""
            generator_code = ""
            module_name = ""
            file_url = ""

            try:
                self.processed_file_path = ""

                # Save the file upload from client to local
                new_path = save_raw_to_local(
                    os.path.join(
                        self.UPLOAD_FROM_CLIENT_DIRECTORY,
                        datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    ),
                    file,
                )

                # Read file in location
                df_raw_c = read_raw_data(
                    new_path,
                    sheet_name="Gpt_PBcfg.c",
                    engine="openpyxl",
                    header=0,
                    usecols="B:E",
                    skiprows=list(range(1, 100)),
                )

                # Analyze and Generate
                standard_rules_c = list()
                for index, row in df_raw_c.iterrows():
                    combined_string = "\n".join(
                        f"{header}: {str(value)}"
                        for header, value in zip(df_raw_c.columns, row.values)
                    )
                    # For test api now - limit request api
                    if index > 6:
                        break
                    # End test
                    std_rule = self.copilot.gen_standard_rule(combined_string)
                    standard_rules_c.append(std_rule.replace("```", ""))

                source_xtend = self.copilot.generate_source_xtend(standard_rules_c)
                source_code = source_xtend.replace("```xtend\n", "").replace("```", "")

                # Read file in location
                df_raw_h = read_raw_data(
                    new_path,
                    sheet_name="Gpt_Cfg.h",
                    engine="openpyxl",
                    header=0,
                    usecols="B:E",
                    skiprows=list(range(1, 53)),
                )

                # Analyze and Generate
                standard_rules_h = list()
                for index, row in df_raw_h.iterrows():
                    combined_string = "\n".join(
                        f"{header}: {str(value)}"
                        for header, value in zip(df_raw_h.columns, row.values)
                    )
                    # For test api now - limit request api
                    if index > 5:
                        break
                    # End test
                    std_rule = self.copilot.gen_standard_rule(combined_string)
                    standard_rules_h.append(std_rule.replace("```", ""))

                header_xtend = self.copilot.generate_header_xtend(standard_rules_h)
                header_code = header_xtend.replace("```xtend\n", "").replace("```", "")

                # Save the file after handle to location
                self.processed_file_path = save_result_to_local(
                    [standard_rules_c, standard_rules_h],
                    ["Gpt_PBcfg.c", "Gpt_PBcfg.h"],
                    os.path.join(
                        self.SEND_TO_CLIENT_DIRECTORY,
                        datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    ),
                    file,
                )

                generator_code = self.copilot.generate_generate_xtend()

                file_url = f"copilot/gen_standard_rule_api/{os.path.basename(self.processed_file_path)}"

                module_name = "Gpt"

            except Exception as e:
                self.SERVER_LOGGER.log(f"Main error : {e}")
                self.SERVER_LOGGER.log(f"\n=> {traceback.format_exc()}")
                raise ServerException(f"Router _Gen_Standard_Rule_ fail: {e}")

            finally:
                return JSONResponse(
                    content={
                        "header": header_code,
                        "source": source_code,
                        "generator": generator_code,
                        "module": module_name,
                        "url": file_url,
                    }
                )

        @self.router_copilot.get("/gen_standard_rule_api/{file_name:path}")
        async def download_standard_rule(file_name: str) -> Any:
            try:
                if self.processed_file_path and os.path.exists(
                    self.processed_file_path
                ):
                    return FileResponse(
                        path=self.processed_file_path,
                        filename=file_name,
                        media_type="application/octet-stream",
                        headers={
                            "Content-Disposition": f'attachment; filename="{file_name}"'
                        },
                    )
                else:
                    raise ServerException(f"File response not found")

            except Exception as e:
                self.SERVER_LOGGER.log(f"Main error : {e}")
                self.SERVER_LOGGER.log(f"\n=> {traceback.format_exc()}")
                raise ServerException(f"Router _Download_Standard_Rule_ fail: {e}")



if __name__ =='__main__':
    FastAPI()
    print(UserResponse(response="Hello thos is"))
    print(GenerateCodeRequest(query="ndfnjf;", current_code="huhu"))
    print(UserRequest(query="Nihao ma"))

