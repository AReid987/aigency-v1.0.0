'use client'

import * as React from 'react'
import { Button } from './button'

interface UploadProps {
    onFileSelect: (files: FileList) => void
    accept?: string
    multiple?: boolean
    maxSize?: number
    className?: string
    children?: React.ReactNode
}

const Upload = React.forwardRef<HTMLDivElement, UploadProps>(
    ({ onFileSelect, accept, multiple = false, maxSize, className = '', children }, ref) => {
        const [isDragOver, setIsDragOver] = React.useState(false)
        const fileInputRef = React.useRef<HTMLInputElement>(null)

        const handleDragOver = (e: React.DragEvent) => {
            e.preventDefault()
            setIsDragOver(true)
        }

        const handleDragLeave = (e: React.DragEvent) => {
            e.preventDefault()
            setIsDragOver(false)
        }

        const handleDrop = (e: React.DragEvent) => {
            e.preventDefault()
            setIsDragOver(false)

            const files = e.dataTransfer.files
            if (files.length > 0) {
                handleFiles(files)
            }
        }

        const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
            const files = e.target.files
            if (files) {
                handleFiles(files)
            }
        }

        const handleFiles = (files: FileList) => {
            if (maxSize) {
                const validFiles = Array.from(files).filter(file => file.size <= maxSize)
                if (validFiles.length !== files.length) {
                    console.warn('Some files were too large and were filtered out')
                }
                if (validFiles.length > 0) {
                    const dt = new DataTransfer()
                    validFiles.forEach(file => dt.items.add(file))
                    onFileSelect(dt.files)
                }
            } else {
                onFileSelect(files)
            }
        }

        const openFileDialog = () => {
            fileInputRef.current?.click()
        }

        return (
            <div
                ref={ref}
                className={`upload-area ${isDragOver ? 'dragover' : ''} ${className}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={openFileDialog}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept={accept}
                    multiple={multiple}
                    onChange={handleFileInput}
                    className="hidden"
                />

                {children || (
                    <div className="text-center">
                        <svg
                            className="mx-auto h-12 w-12 text-gray-400"
                            stroke="currentColor"
                            fill="none"
                            viewBox="0 0 48 48"
                        >
                            <path
                                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                                strokeWidth={2}
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                        <div className="mt-4">
                            <p className="text-sm text-gray-400">
                                <Button variant="link" className="font-medium">
                                    Click to upload
                                </Button>
                                {' '}or drag and drop
                            </p>
                            {accept && (
                                <p className="text-xs text-gray-500 mt-1">
                                    {accept.split(',').join(', ')}
                                </p>
                            )}
                            {maxSize && (
                                <p className="text-xs text-gray-500">
                                    Max file size: {Math.round(maxSize / 1024 / 1024)}MB
                                </p>
                            )}
                        </div>
                    </div>
                )}
            </div>
        )
    }
)

Upload.displayName = 'Upload'

export { Upload }
export type { UploadProps }
