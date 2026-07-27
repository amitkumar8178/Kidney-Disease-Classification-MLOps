from src.cnnclassifier import logger
from cnnclassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline, STAGE_NAME



if __name__== '__main__':
    try:
        logger.info(f">>>>>>>>{STAGE_NAME}<<<<<<<<<")  
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f'>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')

    except Exception as e:
        logger.exception(e)
        raise e

