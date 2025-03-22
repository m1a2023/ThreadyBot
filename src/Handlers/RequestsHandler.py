import httpx

#ЗАПРОСЫ ДЛЯ ОТЧЕТОВ
async def get_report_by_project_id(project_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:9000/api/db/reports/project/{project_id}")
        response.raise_for_status()
        report = response.json()
        return report
