import boto3
import pandas as pd
import json
import io

# 1. Configuración de cliente Boto3 para conexión con AWS Academy S3
s3_client = boto3.client(
    's3',
    aws_access_key_id = "My-Key-ID",
    aws_secret_access_key = "My-Secret-Key",
    aws_session_token = "My-Session-Token",
    region_name="us-east-1"
    )
BUCKET_NAME = "my-academy-bucket"

def cargar_y_perfilar_s3(file_key, is_json=False):
    """Descarga archivos desde S3 en memoria y genera un perfilamiento avanzado."""
    print(f"\n==========================================")
    print(f"=== Procesando objeto S3: {file_key} ===")
    print(f"==========================================")
    
    # Descarga el objeto en memoria sin guardarlo en disco[cite: 6]
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    body = response['Body'].read()
    
    # Conversión según la estructura de la fuente (Estructurada vs Semiestructurada)
    if is_json:
        data_json = json.loads(body.decode('utf-8'))
        df = pd.json_normalize(data_json)
    else:
        df = pd.read_csv(io.BytesIO(body))
        
    # --- ADECUACIONES Y EXTENSIÓN DE PERFILAMIENTO (Paso 3) ---
    print(f"\nDimensiones del dataset: {df.shape[0]} filas x {df.shape[1]} columnas")
    
    print("\n[1] Perfil de Tipos de Datos:")
    print(df.dtypes)
    
    print("\n[2] Conteo de Valores Nulos (Inconsistencias):")
    nulos = df.isnull().sum()
    print(nulos[nulos > 0] if not nulos[nulos > 0].empty else "¡No se encontraron valores nulos!")
    
    print("\n[3] Resumen de Estadísticos Descriptivos (Incluyendo categóricas):")
    print(df.describe(include='all').T)
       
    return df

if __name__ == "__main__":

    # Ingesta y perfilamiento del archivo estructurado (.csv)[cite: 4]
    df_transacciones = cargar_y_perfilar_s3('raw/transacciones.csv', is_json=False)
    
    # Ingesta y perfilamiento del archivo semiestructurado (.json)[cite: 4]
    df_logs = cargar_y_perfilar_s3('raw/logs_m2m.json', is_json=True)