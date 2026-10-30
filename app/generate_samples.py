"""Generate three fictional PaisaPath sample advertisements."""

from app.config import OUTPUT_DIR
from app.content_generator import prepare_copy
from app.template_renderer import render_creative

SAMPLE_OFFER = "Example offer for demonstration only"
SAMPLES = (
    {
        "creative_id": "sample-english",
        "product": "Money planning tools",
        "audience": "Everyday planners",
        "language": "English",
    },
    {
        "creative_id": "sample-hindi",
        "product": "पैसों की योजना के साधन",
        "audience": "रोज़मर्रा के योजनाकार",
        "language": "Hindi",
    },
    {
        "creative_id": "sample-marathi",
        "product": "पैशांच्या नियोजनाची साधने",
        "audience": "दररोज नियोजन करणारे",
        "language": "Marathi",
    },
)


def main() -> None:
    """Generate each sample and report its result."""
    output_dir = OUTPUT_DIR / "samples"
    print("Generating PaisaPath sample creatives...")

    for sample in SAMPLES:
        try:
            copy_data = prepare_copy({**sample, "offer": SAMPLE_OFFER})
            output_path = render_creative(copy_data, output_dir)
        except (OSError, ValueError) as error:
            print(f"ERROR {sample['creative_id']}: {error}")
        else:
            print(f"SAVED {output_path}")


if __name__ == "__main__":
    main()
