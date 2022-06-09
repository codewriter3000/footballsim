class PregeneratedObject {
    constructor(max) {
        if(this.constructor === PregeneratedObject){
            throw new Error("Pregenerated Object cannot be instantiated");
        }
        this._max = max;
    }

    /**
     * A multi-line string
     * @private
     */
    _rawText;
    /**
     * Max line number
     * @private
     */
    _max;

    get rawText() {
        return this._rawText;
    }

    set rawText(value) {
        this._rawText = value;
    }

    get max() {
        return this._max;
    }

    set max(value) {
        this._max = value;
    }

    getRandom() {
        const length = this.max ? this.max : this._rawText.split('\n').length;

        return this.rawText.split('\n')
            [Math.floor(Math.random() * length)];
    }
}

export default PregeneratedObject;