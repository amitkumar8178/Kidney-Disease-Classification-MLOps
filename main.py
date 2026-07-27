from src.cnnclassifier import logger
from cnnclassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from cnnclassifier.pipeline.stage_02_base_model import PrepareBaseModelTrainingConfig
from cnnclassifier.pipeline.stage_03_training import ModelTrainingPipeline


STAGE_NAME = 'Data Ingestion'
try:
    logger.info(f">>>>>>>>{STAGE_NAME}<<<<<<<<<")  
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f'>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = 'Prepare Base Model'

try:
    logger.info(f"*******************")
    logger.info(f">>>>>>>>>>{STAGE_NAME}<<<<<<<<<<<<<")
    prepare_base_model = PrepareBaseModelTrainingConfig()
    prepare_base_model.main()
    logger.info(f">>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<")

except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = 'Model Training'

try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_trainer = ModelTrainingPipeline()
   model_trainer.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e