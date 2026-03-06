import subprocess
import os
import uuid
import json
from django.shortcuts import render
from django.http import JsonResponse



TEMP_DIR = "temp_code"
os.makedirs(TEMP_DIR, exist_ok=True)

def run_code_api(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            lang = data.get("language", "python")

            uid = str(uuid.uuid4())[:8]
            output = ""

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            if lang == "python":

                file_path = os.path.join(TEMP_DIR, f"{uid}.py")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)

                result = subprocess.run(
                    ["python", file_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    env=env
                )

                output = result.stdout + result.stderr
                os.remove(file_path)


            elif lang == "java":

                file_path = os.path.join(TEMP_DIR, "Main.java")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)

                compile_proc = subprocess.run(
                    ["javac", file_path],
                    capture_output=True,
                    text=True
                )

                if compile_proc.returncode == 0:

                    run_proc = subprocess.run(
                        ["java", "-cp", TEMP_DIR, "Main"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )

                    output = run_proc.stdout + run_proc.stderr

                else:
                    output = compile_proc.stderr

                class_file = os.path.join(TEMP_DIR, "Main.class")

                if os.path.exists(class_file):
                    os.remove(class_file)

                os.remove(file_path)

            return JsonResponse({"output": output})

        except subprocess.TimeoutExpired:
            return JsonResponse({"output": "Execution timed out (5 seconds)."})

        except Exception as e:
            return JsonResponse({"output": str(e)})

    return JsonResponse({"output": "Invalid request"})

def editor_home(request):
    return render(request, 'onlinecodeeditor.html')